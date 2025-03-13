import streamlit as st
import random
import time

# 配置页面
st.set_page_config(page_title="单词大闯关", page_icon="🍎", layout="centered")

# 游戏的不同页面
if "page" not in st.session_state:
    st.session_state.page = "start"

# 关卡状态
if "stage" not in st.session_state:
    st.session_state.stage = 1  # 1: 匹配游戏, 2: 拼写游戏

# 记录分数
if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0
if "wrong_count" not in st.session_state:
    st.session_state.wrong_count = 0

# **第一页：游戏开始界面**
if st.session_state.page == "start":
    st.markdown("<h1 style='text-align: center;'>单词大闯关 🎮</h1>", unsafe_allow_html=True)
    if st.button("开始游戏"):
        st.session_state.page = "stage1"
        st.experimental_rerun()

# **第一关：单词匹配游戏**
elif st.session_state.page == "stage1":
    st.markdown("<h2 style='text-align: center;'>第一关</h2>", unsafe_allow_html=True)
    
    cvc_words = ["mat", "cut", "kit", "tap", "lip", "tub", "cup", "sad", "jam", "pop", "hug"]
    cvce_words = ["site", "huge", "mate", "cute", "pipe", "cube", "tape", "cub", "kite"]

    st.write("请把单词拖入正确的篮子里：")
    
    cvc_selected = st.multiselect("选择属于 CVC 结构的单词：", cvc_words + cvce_words)
    cvce_selected = st.multiselect("选择属于 CVCe 结构的单词：", cvc_words + cvce_words)
    
    if st.button("提交答案"):
        correct_cvc = set(cvc_selected) == set(cvc_words)
        correct_cvce = set(cvce_selected) == set(cvce_words)
        
        if correct_cvc and correct_cvce:
            st.success("🎉 全部正确！进入下一关！")
            time.sleep(1.5)
            st.session_state.page = "stage2"
            st.experimental_rerun()
        else:
            st.error("❌ 有错误，请检查后再提交！")

# **第二关：拼写游戏**
elif st.session_state.page == "stage2":
    st.markdown("<h2 style='text-align: center;'>第二关</h2>", unsafe_allow_html=True)
    
    word_list = {
        "hen": "🐔", "nut": "🥜", "rug": "🧶", "gum": "🍬", "mud": "🌧️", 
        "wig": "👩", "lip": "👄", "lid": "🛢️", "vet": "🐶", "fox": "🦊", 
        "pot": "🍲", "log": "🌲", "cut": "✂️", "hug": "🤗", "bin": "🗑️"
    }
    
    words = list(word_list.keys())
    random.shuffle(words)
    
    if "word_index" not in st.session_state:
        st.session_state.word_index = 0
    
    current_word = words[st.session_state.word_index]
    st.write(f"图片提示: {word_list[current_word]}")
    user_input = st.text_input("请输入单词:")
    
    if st.button("确认"):
        if user_input.lower() == current_word:
            st.session_state.correct_count += 1
            st.success("✅ 正确！")
        else:
            st.session_state.wrong_count += 1
            st.error(f"❌ 错误！正确答案是 {current_word}")
        
        if st.session_state.word_index < len(words) - 1:
            st.session_state.word_index += 1
            st.experimental_rerun()
        else:
            st.session_state.page = "finish"
            st.experimental_rerun()

# **最后一关：完成界面**
elif st.session_state.page == "finish":
    st.markdown("<h1 style='text-align: center;'>🎉 恭喜完成闯关！🎆</h1>", unsafe_allow_html=True)
    
    st.write(f"✅ 正确答案数: {st.session_state.correct_count}")
    st.write(f"❌ 错误答案数: {st.session_state.wrong_count}")
    
    st.balloons()
    
    if st.button("重新开始"):
        st.session_state.page = "start"
        st.session_state.correct_count = 0
        st.session_state.wrong_count = 0
        st.session_state.word_index = 0
        st.experimental_rerun()
