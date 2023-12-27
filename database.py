import asyncpg
import asyncio
async def create_table(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "main" (
            "xd"  bigint DEFAULT 77,
            "nopre"  TEXT DEFAULT '[978930369392951366, 979353019235840000, 933738517845118976, 966230921084796999]',
            "bperm"  TEXT DEFAULT '[978930369392951366, 979353019235840000, 933738517845118976, 966230921084796999]',
            PRIMARY KEY("xd")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "count" (
            "xd" bigint DEFAULT 1,
            "guild_count" TEXT DEFAULT '{}',
            "cmd_count" TEXT DEFAULT '{}',
            "user_count" TEXT DEFAULT '{}',
            PRIMARY KEY("xd")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "noprefix" (
            "user_id" bigint,
            "servers" TEXT,
            "main" bigint DEFAULT 0,
            PRIMARY KEY("user_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "afk" (
            "user_id" bigint,
            "afkk" TEXT DEFAULT '{}',
            "globally" bigint DEFAULT 0,
            PRIMARY KEY("user_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "warn" (
            "guild_id" bigint,
            "data" TEXT DEFAULT '{}',
            "count" bigint DEFAULT 0,
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "bl" (
            "main" bigint DEFAULT 1,
            "user_ids" TEXT DEFAULT '[]',
            PRIMARY KEY("main")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS prefixes(
            "guild_id" bigint,
            "prefix" TEXT DEFAULT '-',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "titles" (
            "user_id" bigint,
            "title" TEXT,
            PRIMARY KEY("user_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS roles(
            guild_id bigint,
            role bigint DEFAULT 0,
            official bigint DEFAULT 0,
            vip bigint DEFAULT 0,
            guest bigint DEFAULT 0,
            girls bigint DEFAULT 0,
            tag TEXT,
            friend bigint DEFAULT 0,
            custom TEXT DEFAULT '{}',
            ar bigint DEFAULT 0,
            stag TEXT,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS imp(
            guild_id bigint,
            cmd TEXT DEFAULT 0,
            admin TEXT DEFAULT 0,
            kick TEXT DEFAULT 0,
            ban TEXT DEFAULT 0,
            mgn TEXT DEFAULT 0,
            mgnch TEXT DEFAULT 0,
            mgnro TEXT DEFAULT 0,
            mention TEXT DEFAULT 0,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS pfp(
            guild_id bigint,
            channel_id bigint,
            type TEXT,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS todo(
            user_id bigint,
            todo TEXT DEFAULT '[]',
            PRIMARY KEY(user_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS help(
            main bigint DEFAULT 1,
            no bigint,
            PRIMARY KEY(main)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS auto(
            guild_id bigint,
            humans TEXT,
            bots TEXT,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS welcome(
            guild_id bigint,
            channel_id bigint,
            msg TEXT DEFAULT 'Hey $user_mention',
            emdata TEXT DEFAULT '{"footer": {"text": "Gateway Welcome"}, "color": 3092790, "type": "rich", "description": "Hey $user_mention", "title": "Welcome to $server_name"}',
            embed bigint DEFAULT 0,
            ping bigint DEFAULT 0,
            autodel bigint DEFAULT 0,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS auto(
            guild_id bigint,
            humans TEXT,
            bots TEXT,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS toggle(
            guild_id bigint,
            BAN bigint DEFAULT 0,
            BOT bigint DEFAULT 0,
            KICK bigint DEFAULT 0,
            ROLE_CREATE bigint DEFAULT 0,
            ROLE_DELETE bigint DEFAULT 0,
            ROLE_UPDATE bigint DEFAULT 0,
            CHANNEL_CREATE bigint DEFAULT 0,
            CHANNEL_DELETE bigint DEFAULT 0,
            CHANNEL_UPDATE bigint DEFAULT 0,
            MEMBER_UPDATE bigint DEFAULT 0,
            GUILD_UPDATE bigint DEFAULT 0,
            WEBHOOK bigint DEFAULT 0,
            "ALL" bigint DEFAULT 0,
            PRIMARY KEY(guild_id)
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS wl(
                "guild_id" bigint,
                "BAN" TEXT DEFAULT '[]',
                "BOT" TEXT DEFAULT '[]',
                "KICK" TEXT DEFAULT '[]',
                "ROLE CREATE" TEXT DEFAULT '[]',
                "ROLE DELETE" TEXT DEFAULT '[]',
                "ROLE UPDATE" TEXT DEFAULT '[]',
                "CHANNEL CREATE" TEXT DEFAULT '[]',
                "CHANNEL DELETE" TEXT DEFAULT '[]',
                "CHANNEL UPDATE" TEXT DEFAULT '[]',
                "MEMBER UPDATE" TEXT DEFAULT '[]',
                "GUILD UPDATE" TEXT DEFAULT '[]',
                "WEBHOOK" TEXT DEFAULT '[]',
                "ALL" TEXT DEFAULT '[]',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS punish(
                "guild_id" bigint,
                "PUNISHMENT" TEXT DEFAULT 'BAN',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS lockr(
                "guild_id" bigint,
                "role_id" TEXT DEFAULT '[]',
                "bypass_uid" TEXT DEFAULT '[]',
                "bypass_rid" TEXT DEFAULT '[]',
                "m_list" TEXT DEFAULT '{}',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS raidmode(
                "guild_id" bigint,
                "toggle" bigint DEFAULT 0,
                "time" bigint DEFAULT 10,
                "max" bigint DEFAULT 15,
                "PUNISHMENT" TEXT DEFAULT 'KICK',
                "lock" bigint DEFAULT 0,
                "lockdown" bigint DEFAULT 1,
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "logs" (
                "guild_id"	bigint,
                "mod"	bigint,
                "role"	bigint,
                "channel"	bigint,
                "server"	bigint,
                "member"	bigint,
                "message"	bigint,
                "antinuke"	bigint,
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "gwmain" (
                "guild_id"  bigint,
                "gw" TEXT DEFAULT '{}',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "invc" (
                "guild_id"  bigint,
                "vc" TEXT DEFAULT '{}',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "bot" (
                "bot_id"  bigint,
                "totaltime" bigint DEFAULT 0,
                "server" TEXT DEFAULT '{}',
                "user" TEXT DEFAULT '{}',
                PRIMARY KEY("bot_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "setup" (
            "guild_id"  bigint,
            "channel_id" bigint,
            "msg_id" bigint,
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "247" (
            "guild_id"  bigint,
            "channel_id" bigint,
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "pl" (
            "user_id"  bigint,
            "pl" TEXT DEFAULT '{}',
            PRIMARY KEY("user_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "user" (
            "user_id"  bigint,
            "totaltime" bigint DEFAULT 0,
            "server" TEXT DEFAULT '{}',
            "friend" TEXT DEFAULT '{}',
            "artist" TEXT DEFAULT '{}',
            "track" TEXT DEFAULT '{}',
            PRIMARY KEY("user_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "panel" (
            "guild_id"  bigint,
            "channel_id" bigint,
            "msg_id" bigint,
            "opencategory" bigint,
            "closedcategory" bigint,
            "claimedrole" bigint,
            "supportrole" bigint,
            "pingrole" bigint,
            "name" TEXT,
            "msg" TEXT DEFAULT '\nTo create a ticket interact with the button below 📩',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "ticket" (
            "guild_id"  bigint,
            "name" TEXT,
            "count" bigint DEFAULT 0000,
            "opendata" TEXT DEFAULT '{}',
            "closeddata" TEXT DEFAULT '{}',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "ignore" (
            "guild_id"  bigint,
            "cmd" TEXT DEFAULT '[]',
            "channel" TEXT DEFAULT '[]',
            "user" TEXT DEFAULT '[]',
            "role" TEXT DEFAULT '[]',
            "module" TEXT DEFAULT '[]',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "bypass" (
            "guild_id"  bigint,
            "bypass_users" TEXT DEFAULT '{}',
            "bypass_roles" TEXT DEFAULT '{}',
            "bypass_channels" TEXT DEFAULT '{}',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "srmain" (
            "guild_id"  bigint,
            "data_button" TEXT DEFAULT '[]',
            "data_dropdown" TEXT DEFAULT '[]',
            PRIMARY KEY("guild_id")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "testlist" (
            "test"  bigint,
            "ls" TEXT DEFAULT '[]',
            PRIMARY KEY("test")
        )
    ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "messages_db" (
                "guild_id"  bigint,
                "messages" TEXT DEFAULT '{}',
                "daily_messages" TEXT DEFAULT '{}',
                "bl_channels" TEXT DEFAULT '[]',
                PRIMARY KEY("guild_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "prmain" (
                "user_id"	bigint,
                "duration"	bigint,
                "total"	bigint,
                "guilds"	TEXT DEFAULT '[]',
                "tier"	TEXT,
                PRIMARY KEY("user_id")
        )
        ''')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS "prguild" (
                "guild_id"	bigint,
                "activator"	bigint,
                "since"	bigint,
                "till"	bigint,
                PRIMARY KEY("guild_id")
        )
        ''')
    return True

if __name__ == "__main__":
    async def xd():
        conn = await asyncpg.connect('postgres_uri')
        await create_table(conn)
        query = 'SELECT * FROM  "247" WHERE guild_id=1036594185442177055'
        i = await conn.fetchall(query)
        for j, k in i:
            print(j, k)
