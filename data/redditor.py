class Redditor:
    def __init__(self):
        self.username = ''
        self.post_karma = 0
        self.comment_karma = 0
        self.created_utc = 0
        self.has_verified_email = False
        self.is_default_icon = True
        self.is_mod = False
        self.is_gold = False

        self.comments = []
        self.submissions = []

        self.is_bot = False
