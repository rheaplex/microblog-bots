import random
import yaml
import sqlite3
import sys

import statusnet

class MicroblogBot(object):
    """A bot that periodically posts updates and responds to @messages"""
    
    LAST_MESSAGE_RESPONDED_TO = 'last_message_responded_to'
    DEFAULT_RUN_FREQUENCY = 1

    def __init__(self, config_path):
        """Connect to the database used to persist the bot state"""
        self.config = yaml.load(open(config_path))
        self.configure()
        self.conn = sqlite3.connect(self.config['database'])
        self.conn.execute('''create table if not exists bot_state
                             (name text primary key, value text)''')
        self.api = statusnet.StatusNet(self.microblog_server,
                                       username=self.microblog_username,
                                       password=self.microblog_password)

    def configure(self):
        """Load the configuration and set up the system"""
        self.database_path = self.config['database']
        self.microblog_server = self.config['server']
        self.microblog_username = self.config['username']
        self.microblog_password = self.config['password']
        self.ignore = self.config.get('ignore', '').split()
        self.run_frequency = \
            int(self.config.get('run_frequency',
                                MicroblogBot.DEFAULT_RUN_FREQUENCY))

    def db_get(self, key, default=''):
        """Get the value from the database or,return default if not set"""
        result = self.conn.execute("select value from bot_state where name=?",
                                   (key,))
        try:
            # Stringify the buffer. For any pickled (protocol 0) values...
            value = str(result.fetchone()[0])
        except:
            value = default
        return value

    def db_set(self, key, value):
        """Set the value in the database"""
        self.conn.execute("insert or replace into bot_state values(?, ?)",
                          (key, value))
        self.conn.commit()

    def update_state(self):
        """Update any state needed before running"""
        pass

    def should_respond_to(self, message):
        """Decide whether to respond to the message or not"""
        return not message['in_reply_to_screen_name'] in self.ignore

    def generate_response(self, message):
        """Generate a response to the @message"""
        return "Hi @%s !" % message['user']['screen_name']

    def respond_to_messages(self):
        """Respond to messages sent since the bot last ran,
           or ignore all if being run for the first time to avoid flooding."""
        last_responded_to = self.db_get(MicroblogBot.LAST_MESSAGE_RESPONDED_TO,
                                        None)
        messages = self.api.statuses_replies(since_id=last_responded_to)
        if messages:
            if last_responded_to != None:
                last_responded_to = int(last_responded_to)
                # Reverse the order of messages to get oldest to newest
                messages = messages[::-1]
                for message in messages:
                    if (message['id'] > last_responded_to) \
                            and self.should_respond_to(message):
                        try:
                            response = self.generate_response(message)
                            #self.api.statuses_update(response, 
                            #               in_reply_to_status_id=message['id'])
                            print response
                        except Exception, e:
                            pass
            new_last_responded_to = max([message['id'] for message in messages])
            self.db_set(MicroblogBot.LAST_MESSAGE_RESPONDED_TO,
                        new_last_responded_to)

    def generate_update(self):
        """Generate a message to be posted as an update"""
        return None

    def post_update(self):
        """Generate a message and post it as an update"""
        update = self.generate_update()
        if update:
            self.api.statuses_update(update)

    def should_post(self):
        """Should the bot generate a new post?"""
        # Handle the run frequency being set to zero
        return self.run_frequency and \
            (random.randint(1, self.run_frequency) == 1)

    def run_once(self):
        self.update_state()
        self.respond_to_messages()
        posting = self.should_post()
        if posting:
            self.post_update()
        return posting


class MicroblogFollowerBot(MicroblogBot):
    """A bot that follows a user and comments on their posts"""

    LAST_UPDATE_COMMENTED_ON = 'last_commented_on'

    def configure(self):
        """Load the configuration and set up the system"""
        super(MicroblogFollowerBot, self).configure()
        self.microblog_follow_user = self.config['follow']
    
    def generate_comment(self, message):
        """Generate a comment on the update by the followed user"""
        return "Hi %s !" % message.user

    def should_comment(self, message):
        """Should the bot comment on the message?"""
        return not (message['in_reply_to_screen_name'] or
                    (message['text'].strip()[0] == "@"))

    def comment_on_updates(self):
        """Comment on updates posted by the followed user since bot last ran,
           or ignore all if being run for the first time to avoid flooding"""
        last_responded_to = \
            self.db_get(MicroblogFollowerBot.LAST_UPDATE_COMMENTED_ON, None)
        if not self.microblog_follow_user:
            print "No user id specified to follow."
            sys.exit(2)
        messages = self.api.statuses_user_timeline(\
            screen_name=self.microblog_follow_user,
            since_id=last_responded_to)
        if messages:
            if last_responded_to != None:
                last_responded_to = int(last_responded_to)
                # Reverse the order of messages to get oldest to newest
                messages = messages[::-1]
                for message in messages:
                    if (message['id'] > last_responded_to) \
                            and self.should_comment(message):
                        try:
                            response = self.generate_comment(message)
                            self.api.statuses_update(response,
                                                     in_reply_to_status_id=message['id'])
                        except Exception, e:
                            print str(e)
            new_last_responded_to = max([message['id'] for message in messages])
            self.db_set(MicroblogFollowerBot.LAST_UPDATE_COMMENTED_ON,
                        new_last_responded_to)

    def run_once(self):
        posting = super(MicroblogFollowerBot, self).run_once()
        if posting:
            posting = self.comment_on_updates()
        return posting


def run_once(bot_class):
    """Utility method to run a bot"""
    if len(sys.argv) != 2:
        print "Please specify path to yaml config file as first argument."
        sys.exit(2)
    config_path = sys.argv[1]
    bot = bot_class(config_path)
    bot.run_once()
