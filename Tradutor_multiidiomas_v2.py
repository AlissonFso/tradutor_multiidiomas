import speech_recognition as sr
from selenium import webdriver
from time import sleep
import pyttsx3

speaker = pyttsx3.init() #inicia serviço biblioteca
voices = speaker.getProperty('voices') #metodo de voz

frase_ok = ''
sl = "pt"
# target language:
tl = "en"
# operation:
operation = "translate"
element= ''
voz = ''

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
wd = webdriver.Chrome(options = options)





def parse_string(text):
    """Replace the following characters in the text"""
    special_characters = (
            ("%", "%25"),
            (" ", "%20"),
            (",", "%2C"),
            ("?", "%3F"),
            ("\n", "%0A"),
            ('\"', "%22"),
            ("<", "%3C"),
            (">", "%3E"),
            ("#", "%23"),
            ("|", "%7C"),
            ("&", "%26"),
            ("=", "%3D"),
            ("@", "%40"),
            ("#", "%23"),
            ("$", "%24"),
            ("^", "%5E"),
            ("`", "%60"),
            ("+", "%2B"),
            ("\'", "%27"),
            ("{", "%7B"),
            ("}", "%7D"),
            ("[", "%5B"),
            ("]", "%5D"),
            ("/", "%2F"),
            ("\\", "%5C"),
            (":", "%3A"),
            (";", "%3B")
        )
    
    for pair in special_characters:
        text = text.replace(*pair)    

    return text


def lingua(idioma_saida):

    idioma_characters = (
        ('africano','af'),
        ('albanês','sq'),
        ('amárico','am'),
        ('árabe','ar'),
        ('armênio','hy'),
        ('azerbaijano','az'),
        ('basco','eu'),
        ('bielorrusso','be'),
        ('bengali','bn'),
        ('bósnio','bs'),
        ('búlgaro','bg'),
        ('catalão','ca'),
        ('cebuano','ceb'),
        ('chinês (simplificado)','zh-CN'),
        ('chinês (tradicional)','zh-TW'),
        ('córsico','co'),
        ('croata','hr'),
        ('checo','cs'),
        ('dinamarquês','da'),
        ('holandês','nl'),
        ('ingles','en'),
        ('esperanto','eo'),
        ('francês','fr'),
        ('galego','gl'),
        ('georgiano','ka'),
        ('alemão','de'),
        ('grego','el'),
        ('havaiano','haw'),
        ('indonésio','id'),
        ('irlandês','ga'),
        ('italian','it'),
        ('japonês','ja'),
        ('macedônio','mk'),
        ('maltês',	'mt'),
        ('maori','mi'),
        ('mongol','mn'),
        ('myanmar','my'),
        ('nepalês','ne'),
        ('norueguês','no'),
        ('nianja','ny'),
        ('oriá','or'),
        ('pashto','ps'),
        ('persa','fa'),
        ('polonês','pl'),
        ('português','pt'),
        ('punjabi','pa'),
        ('romeno','ro'),
        ('russo','ru'),
        ('samoano','sm'),
        ('gaélico escocês','gd'),
        ('sérvio','sr'),
        ('sesoto','st'),
        ('espanhol','es')
    )

    for pair in idioma_characters:
        
        idioma_saida = idioma_saida.replace(*pair)

    return idioma_saida


def copiar_traducao():
    global element
    try:
        element = wd.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div').text
        print('element = ', element.replace(' volume_up\ncontent_copy\nshare',''))
        element = element.replace(' volume_up\ncontent_copy\nshare','')
    except:
        copiar_traducao()
    else: return



#Função para ouvir e reconhecer a fala
def traduzir(link):
    wd.get(link)
    copiar_traducao()
    return 



def find_voz(lin):
    global voz
    aux = False
    for voice in voices:
        if lin in voice.id:
            voz = voice.id
            aux = True
    
    if aux == True:
        return
    else: voz = voices[0].id





def ouvir_microfone(sl, y):
    
    global element, voz

    microfone = sr.Recognizer()
    
    #usando o microfone
    with sr.Microphone() as source:
        
      
        microfone.adjust_for_ambient_noise(source)
       
        print(" - ")
         
        audio = microfone.listen(source)
        
    try:
       
        #Passa a variável para o algoritmo reconhecedor de padroes
        frase = microfone.recognize_google(audio,language=sl)
        
       
        #Retorna a frase pronunciada
        frase_1 = frase.replace('asterisco', '*')
        #frase_1 = frase.replace('risco', '*')
        frase_2 = frase_1.replace('jogo da velha', '#')
        frase_ok = frase_2.replace('jogo-da-velha', '#')
        print(frase_ok)
        texto = parse_string(frase_ok)
        # f-string with the variables:
        sl = 'auto'
        tl = lingua(y)
        link = f"https://translate.google.com/?sl={sl}&tl={tl}&text={texto}&op={operation}"
        traduzir(link)
        speaker.setProperty('voice', voz) #define a voz padrao, no meu caso o portugues era o[2] (iniciando do zero)
        rate = speaker.getProperty('rate')
        speaker.setProperty('rate', rate-30)
        speaker.say(element) #define o texto que será lido
        speaker.runAndWait()
        
        
    #Se nao reconheceu o padrao de fala, exibe a mensagem
    except Exception as e:
        print("ERRO !!")
        print(e)
        
    return 




 
def main():
    aux = 0
    for voice in voices:
        print(voice.id) #traz os idiomas de voz instalados em sua maquina
    sl = input('Entre com o idioma de origem: ')
    y = input('Entre com o idioma de destino: ')
    while(True):
        
        if sl.lower() == 'portugues':
            sl = 'pt-BR'
            
        elif sl.lower() == 'espanhol':
            sl = 'es-ES'
            
        elif sl.lower() == 'ingles':
            sl = 'en-US'



        if y.lower() == 'portugues':
            voz_id = find_voz('PT')
        elif y.lower() == 'espanhol':
            voz_id = find_voz('ES')
        elif y.lower() == 'ingles':            
            voz_id = find_voz('EN')    

        ouvir_microfone(sl, y)
        

main()