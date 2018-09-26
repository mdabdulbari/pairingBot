import sqlite3

class DataBase():
    def __init__(this):
        this.connection = sqlite3.connect('pairing_bot.sqlite')

    def save(this, channel, list_of_combinations):
        this.connection.execute("INSERT INTO channels (channel) VALUES ('%s');" % (channel))
        this.connection.commit()
        channels = this.connection.execute("SELECT * FROM channels;")
        for channel1 in channels:
            if(channel1[1] == channel):
                channel_id = channel1[0]
                break
        for i in range(len(list_of_combinations)):
            string_of_current_combination = ",".join(list_of_combinations[i])
            print(string_of_current_combination)
            this.connection.execute("INSERT INTO combinations (day, channel_id, combination) VALUES (%d, %d, '%s');" % (i, channel_id, string_of_current_combination))
        this.connection.commit()

    def get_combination(this, index, channel):
        combination = this.connection.execute("SELECT combinations.combination FROM channels JOIN combinations ON channels.id=combinations.channel_id WHERE channel = '%s' AND day = %d;" % (channel, index))
        for combination1 in combination:
            return combination1[0]
