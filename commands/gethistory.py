import functions.constants
from classes.Log import Log

async def gethistory(message):
    """
    Gets the history of races. Must be an admin

    Parameters
    ----------
    message : discord.message.Message
        A discord message containing our command

    Returns
    -------
    Nothing
    """
    logger = Log()

    if message.content.startswith("!gethistory"):
        if message.author.id not in functions.constants.ADMINS:
            return

        try:
            with open(functions.constants.RACE_FILE, 'r') as f:
                m_msg = f.read()
                f.close()

            chunks = m_msg.split('\n')
            chunk = "`\n"
            counter = 0
            while counter < len(chunks):
                while counter < len(chunks) and len(chunk + chunks[counter]) < functions.constants.MAX_MSG_LEN - 4:
                    chunk += chunks[counter] + "\n"
                    counter += 1
                await message.channel.send(chunk + '`')
                chunk = "`\n"

        except Exception as e:
            emsg = "Unable to read from %s - %s" % (functions.constants.RACE_FILE, str(e))
            logger.show(emsg, functions.constants.LOG_CRITICAL)