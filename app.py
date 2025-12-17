import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
import time

# 設定網頁標題
st.set_page_config(page_title="Azure TTS Live Demo", page_icon="🔊")

st.title("🔊 Azure 雲端發聲服務 (Korea Central)")
st.write("本服務由 Ubuntu 24.04 VM + Docker 驅動")

# 從環境變數讀取 Key (資安最佳實踐)
SPEECH_KEY = os.getenv('SPEECH_KEY')
SPEECH_REGION = os.getenv('SPEECH_REGION')

# 介面設計
text_input = st.text_area("請輸入文字 (中文/English)", height=150, value="你好，這是來自 Azure 韓國機房的即時語音合成。")

# 語音選單
voice_map = {
    "台灣女聲 (曉臻)": "zh-TW-HsiaoChenNeural",
    "台灣男聲 (雲哲)": "zh-TW-YunJheNeural",
    "美國女聲 (Jenny)": "en-US-JennyNeural"
}
selected_voice = st.selectbox("選擇語音角色", list(voice_map.keys()))

if st.button("開始合成"):
    if not SPEECH_KEY or not SPEECH_REGION:
        st.error("❌ 錯誤：未偵測到 API Key，請檢查容器環境變數。")
    else:
        try:
            # 設定 Azure Speech Config
            speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
            speech_config.speech_synthesis_voice_name = voice_map[selected_voice]
            
            # 設定輸出為檔案
            file_name = "output.wav"
            audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

            # 執行合成
            with st.spinner('Azure AI 正在運算中...'):
                result = synthesizer.speak_text_async(text_input).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                st.success("✅ 合成成功！")
                audio_file = open(file_name, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
                audio_file.close()
            else:
                st.error(f"合成失敗: {result.reason}")

        except Exception as e:
            st.error(f"系統錯誤: {e}")