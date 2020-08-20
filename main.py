import discord
from operacjeNaPlikach import odczytaj_plik, nadpisz_plik

client = discord.Client()

# https://discord.com/api/oauth2/authorize?client_id=734405121118699543&permissions=1342700608&scope=bot

@client.event
async def on_member_join(member):
    """
    Powyższa funkcja sprawdza czy do serwera dołączyła nowa
    osoba i wysyła na kanale ogólnym wiadomość powitalną.
    """
    kanal = discord.utils.get(member.guild.channels, name="kanał-ogólny")
    await kanal.send(f'Witamy, witamy {member.mention} w naszych skromnych progach.\n'
                     f'Rozsiądź się wygodnie i spocznij w ławie biesiadnej, przygotuję strawę.')


@client.event
async def on_raw_reaction_add(reakcja):
    """
    Powyższa funkcja sprawdza czy została dodana reakcja do posta.
    jeśli została dodana określona reakcja to przyznaje nadawcy
    rangę przypisaną do danej rangi
    """
    wiadomosc = odczytaj_plik("Wiadomosc_z_rangami")
    if reakcja.message_id == int(wiadomosc):
        id_reakcji = reakcja.guild_id
        lista_rol = discord.utils.find(lambda g: g.id == id_reakcji, client.guilds)
        if reakcja.emoji.name == 'TawernaRPG':
            rola = discord.utils.get(lista_rol.roles, name='Tawerna RPG')
        elif reakcja.emoji.name == 'KrysztalyCzasu':
            rola = discord.utils.get(lista_rol.roles, name='Kryształy Czasu')
        else:
            rola = None
        if rola is not None:
            uzytkownik = discord.utils.find(lambda m: m.id == reakcja.user_id, lista_rol.members)
            await uzytkownik.add_roles(rola)
        else:
            pass


@client.event
async def on_raw_reaction_remove(reakcja):
    """
    Powyższa funkcja sprawdza czy została usunięta reakcja z posta.
    jeśli została usunięta określona reakcja to odejmuje nadawcy
    rangę przypisaną do danej rangi
    """
    wiadomosc = odczytaj_plik("Wiadomosc_z_rangami")
    if reakcja.message_id == int(wiadomosc):
        id_reakcji = reakcja.guild_id
        lista_rol = discord.utils.find(lambda g: g.id == id_reakcji, client.guilds)
        if reakcja.emoji.name == 'TawernaRPG':
            role = discord.utils.get(lista_rol.roles, name='Tawerna RPG')
        elif reakcja.emoji.name == 'KrysztalyCzasu':
            role = discord.utils.get(lista_rol.roles, name='Kryształy Czasu')
        else:
            role = None

        if role is not None:
            uzytkownik = discord.utils.find(lambda m: m.id == reakcja.user_id, lista_rol.members)
            await uzytkownik.remove_roles(role)


async def status(nowy_status=""):
    """
    Powyższa funkcja iteruje statusy
    :param nowy_status:
    :return:
    """
    await client.wait_until_ready()
    from operacjeNaPlikach import opis, nowy_opis
    from itertools import cycle
    if not nowy_status:
        lista_opisow = cycle(opis())
        while not client.is_closed():
            opis = next(lista_opisow)
            await client.change_presence(status=discord.Status.idle, activity=discord.Game(opis))
            import asyncio
            await asyncio.sleep(300)
    elif nowy_status:
        lista_opisow = cycle(opis())
        while not client.is_closed():
            opis = next(lista_opisow)
            await client.change_presence(status=discord.Status.idle, activity=discord.Game(opis))
            import asyncio
            await asyncio.sleep(300)


@client.event
async def on_ready():
    """
    Powyższa funkcja informuje o zalogowaniu
    :return:
    """
    print(f'Zalogowano jako: {client.user.name}')
    print(f"Id użytkownika: {client.user.id}")
    print('----------------------------------')
    kanal = discord.utils.get(client.get_all_channels(), name="kanał-ogólny")
    if odczytaj_plik("Wiadomosc_z_rangami") == "":
        print('Brak identyfikatora wiadomości.. tworzę nową wiadomość')
        wyslana_wiadomosc = await kanal.send(
            f'Witajcie w mojej karczmie zdrożeni podróżnicy, witam w moich skromnych progach. \n'
            f'Jeśli sobie życzycie piwa pienistego to zapraszam do kontuaru, a zaraz coś znajdę. '
            f'Jeśli jednak życzycie sobie dołączyć do jednej z dwóch frakcji znajdujących się w '
            f'poniższym przybytku to pozwolę sobie dam obie przedstawić.\n'
            f'<:TawernaRPG:737758888874606685> '
            f'Pierwsza frakcja to tawerniacy. Piją, palą, chulają i swawolą. \n'
            f'https://tawerna.rpg.pl/forum/ ich tablicą ogłoszeń, którą obserwują w poszukiwaniu nowości. \n'
            f'https://tawerna.rpg.pl/ i https://www.facebook.com/TawernaRPG/ to miejsce gdzie ich także znaleźć '
            f'można. \n '
            f'<:KrysztalyCzasu:737761618342969426> '
            f'Druga frakcja to bywalcy z Kryształów Czasu. Mroczna kraina gdzie mróz i skwar doskwierają. \n'
            f'https://krysztalyczasu.pl/forum/ ich tablicą ogłoszeń, na której wici rozpuszczają o nowych wyzwaniach. \n'
            f'https://krysztalyczasu.pl/ i https://www.facebook.com/sagakrysztalyczasu to natomiast świat który '
            f'zamieszkują na codzień. \n '
            f'\n'
            f'Do kogo dołączysz podróżniku?:')
        await discord.Message.pin(wyslana_wiadomosc)
        nadpisz_plik("Wiadomosc_z_rangami", str(wyslana_wiadomosc.id))
        await wyslana_wiadomosc.add_reaction("<:TawernaRPG:737758888874606685>")
        await wyslana_wiadomosc.add_reaction("<:KrysztalyCzasu:737761618342969426>")

    else:
        print('Znaleziono identyfikator wiadomości.. zaczynam obsługę')


# Tu trzeba wstawić token 0auth
def OdczytajToken():
    """
    Powyższa funkcja odczytuje token Oauth zapisany w pliku tekstowym
    :return:
    """
    with open("Dane/token_0auth.txt", "r") as token:
        odczytany_token = token.readlines()
        return odczytany_token[0].strip()


client.loop.create_task(status())
client.run(OdczytajToken())
