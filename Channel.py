class Channel():
    def __init__(this, channel_id):
        this.channel_id = channel_id
        this.index = 0
        this.skip = False

    def increment_index(this):
        this.index += 1

    def get_channel_id(this):
        return this.channel_id
    
    def get_index(this):
        return this.index

    def skip(this):
        this.skip = True

    def reset_skip(this):
        this.skip = False
    
    def should_skip(this):
        return this.skip
