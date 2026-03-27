import streamlit as st
import Koreainvestment as mojito
import pandas as pd
import time

# 1. 페이지 설정
st.set_page_config(page_title="My Trading Bot", layout="wide")
st.title("📈 실시간 주식 자산 대시보드")

# 아까 메모장에 적어둔 정보를 여기에 넣어줘
KEY = st.secrets["KOREAINVEST_KEY"]
SECRET = st.secrets["KOREAINVEST_SECRET"]
ACC_NO = st.secrets["KOREAINVEST_ACC_NO"]


# 한국투자증권 연결 
broker = mojito.KoreaInvestment(
    api_key=KEY ,
    api_secret=SECRET ,
    acc_no=ACC_NO ,
    mock=False
)

# 3. 사이드바 - 새로고침 버튼
if st.sidebar.button('수동 새로고침'):
    st.rerun()

# 4. 데이터 가져오기 함수
def get_balance():
    res = broker.fetch_balance()
    # 총 자산 정보
    total_data = res['output2'][0]
    # 보유 종목 정보
    stock_list = res['output1']
    return total_data, stock_list

try:
    total, stocks = get_balance()

# 기존 코드를 지우고 이걸로 바꿔봐!
    col1, col2, col3 = st.columns(3)
    col1.metric("총 평가금액", f"{int(total.get('tot_evlu_amt', 0)):,} 원")
    col2.metric("총 수익금", f"{int(total.get('evlu_pfls_smtl_amt', 0)):,} 원")
    
    # 수익률 데이터 이름이 다를 수 있으니 안전하게 가져오기
    rt_value = total.get('evlu_pfls_rt') or total.get('pft_rt') or "0"
    rt = float(rt_value)
    col3.metric("수익률", f"{rt:.2f}%", delta=f"{rt:.2f}%")

    st.divider()

    # 6. 보유 종목 상세 내역 (Table)
    st.subheader("📝 보유 종목 상세")
    if not stocks:
        st.write("현재 보유 중인 종목이 없습니다.")
    else:
        df = pd.DataFrame(stocks)
        # 보기 편하게 컬럼명 변경 및 필요한 것만 추출
        df = df[['prdt_name', 'pdno', 'hldg_qty', 'pchs_avg_pric', 'prpr', 'evlu_pfls_rt']]
        df.columns = ['종목명', '코드', '보유수량', '매수평균가', '현재가', '수익률(%)']
        
        # 표 출력
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

st.caption(f"최근 업데이트 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
