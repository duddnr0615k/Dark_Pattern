class check_info():
    def Check_info(self,info):
        result = []
        phone = ['phone', '휴대폰', '휴대폰 번호', '전화번호', '전화 번호']
        email = ['email', '이메일', '이메일 주소', '전자메일 주소']
        gender = ['성별', 'gender']
        arr = ['주소', '배송 주소', '배송지 주소']
        health = ['건강정보', '건강 정보']
        birth = ['생년월일', '생일']
        id = ['주민등록번호']
        driver_id = ['운전면허', '면허']
        device = ['기기정보', '기기 정보', '디바이스']
        no_privacy = ['개인정보처리방침없음']
        cookie_info = ['쿠키']
        name = ['이름','성명']
        credit_info = ['계좌번호', '계좌 번호', '카드번호', '카드 번호']
        location = ['위치정보', '위치 정보']
        travel = ['여권번호', '여권 번호']
        body_info = ['신체정보', '신체 정보', '몸무게', '신장']
        risk_normal = '보통'
        risk_hard = '신중'

        dic = [phone, email, gender, arr, health, birth, id, driver_id, device, no_privacy, cookie_info, name,
               credit_info, location, travel, body_info]
        for list1 in dic:
            for word in list1:
                if word in info:
                    if list1[0] not in result:
                        result.append(list1[0])
        # 위험도가 1등급인 경우  '주의'등급
        if '주민등록번호' in result or '여권번호' in result or '운전면허' in result or '건강정보' in result or '계좌번호' in result or '위치정보' in result:
            result.append(risk_hard)
            return result
        # 위험도 2등급의 개수가 6개 이상일 경우 '주의' 등급
        compare_normal = ['주소', 'phone', 'email', '생년월일', '이름', '신체정보', '성별']
        marge_normal = list(set(result).intersection(compare_normal))
        if len(marge_normal) >= 6:
            marge_normal.append(risk_hard)
            return marge_normal
        elif len(marge_normal) == 0:
            return result
        else:
            if '개인정보처리방침없음' in result:
                return result
            # 평시상태는 보통
            result.append(risk_normal)
            return result
