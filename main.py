from huggingface_hub import snapshot_download
import sounddevice as sd
from scipy.io.wavfile import write
import os , sys, requests
from getSysInfo import SystemInfo

def modCheck(name, platforms, src, tar):

        base_path = f"/home/{os.listdir("/home")[0]}/.cache/huggingface/hub/{name}/"
        snapshot = os.listdir(f"{base_path}/snapshots/")[0]
        model_path = f"{base_path}/snapshots/{snapshot}/"

        if (os.path.exists(f"{model_path}") == False):
            try:
                response = requests.head(f"https://huggingface.co/{name}")
                if ("tf" in (platforms[0] or platforms[1])) == False:
                    snapshot_download(repo_id=f"{name}", ignore_patterns="*.t5")
                else:
                    snapshot_download(repo_id=f"{name}")
                if "opus-mt" in name:
                    print("Would you like to download the opposite language pair? (Y/n)")
                if input().lower() != "n":
                    try:
                        response = requests.head(f"https://huggingface.co/Helsinki-NLP/opus-mt-{tar}-{src}")
                        snapshot_download(repo_id=f"Helsinki-NLP/opus-mt-{tar}-{src}")
                    except requests.RequestException as e:
                        if "emporary failure in name resolution" in {e}:
                            print("Check your internet connection")
                        else:
                            print(f"Error: {e}")

            except requests.RequestException as e:
                if "emporary failure in name resolution" in {e}:
                    print("Check your internet connection")
                else:
                    print(f"Error: {e}")

def run_Transcriber(name):

    '''from getSysInfo in some way
    Rank = {'cpu': ('god knows', 6.4, 'fp16'), 'gpu': ('cuda', 6, 'fp16'), 'tpu': ('tf', 0, 'int8')}

    '''

    '''
        if platform not in model.supported_platforms:
            temp = perfRank.pop(max(perfRank, key=perfRank.get)
            while max(temp, ...) not in model.supported_platforms:
                temp.pop(max(temp, ...))
                if temp.is_empty() == True:
                    #no supported platforms, change model
            platform = max(temp, key=temp.get).platform
        
        
    '''

    key, value = next(iter(Rank.items()))
    platforms = [value[0] for key, value in Rank.items()]
    precission = value[2]

    if name in transformer_models:
            modCheck(name,platforms,'','')
    
    if name == "Systran/faster-whisper-medium":

        from faster_whisper import WhisperModel
        model_size = "large-v3"#temp, gpu vram dep with user override

        if (platform in name.supported_platforms for platform in platforms) == None: #check if platform is supported from csv file
            print("No supported platform, change model")
            return
        else:
            model = WhisperModel(model_size, platforms, precission)
            



    #such great docs on how this works
        
    #transform lang codes

    #WHY TF IS THIS NOT FUCKING STANDARTISED?????

    #modify public vars for codes
    

'''def run_Translator(src, tar):

    same compatability shit

    init and use translator
        will someday impliment weighted words database to go with it

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        if not use the dir path to set up

    such great docs on how this works

    modify text.md with new text
        you do know you have to write an obsidian clone (or just a plugin pref) to even use this outside the terminal, right?

def record():

    i = 0
    freq = 44100
    duration = 2

    print("Talk now")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()

    write(f"recording{i}.wav", freq, recording)
    i+=1
    '''

def main():
    system = SystemInfo()
    system.get_system_info()
    print(system.gpu.vendor, "1")

    tar = "en"

    transformer_models = {"Helsinki-NLP"}

    models = {
        "Transcriber": f"Systran/faster-whisper",
        "Translator": f"Helsinki-NLP/opus-mt-{any}-{tar}"
    }

    run_Transcriber(models["Transcriber"].value())

    if f"Helsinki-NLP/opus-mt-{any}-{tar}" in models.values():
        try:
            from transformers import MarianMT, MarianTokenizer
            run_Transcriber()
        except:
            modCheck("fHelsinki-NLP/opus-mt-{any}-{tar}")





