import MySQLdb

class MEMBER:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f"MEMBER(username='{self.username}', password='{self.password}', name='{self.name}', email='{self.email}')"
    
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        if not username:
            raise ValueError("username(로그인 아이디) 입력해라")
        self.__username = username

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        if not password:
            raise ValueError("password 입력해라")
        self.__password = password

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("name 실명 입력해라")
        self.__name = name
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        if not email:
            raise ValueError("email 입력해라")
        self.__email = email


class PRODUCT:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("물건 이름 입력해라")
        self.__name = name
    


class ServiceDAO:
    def __init__(self):
        self.db = None
    
    def connect(self):
        self.db = MySQLdb.connect(host='localhost', user='AAA', password='1111', db='EXAM01', charset='utf8')

    def disconnect(self):
        if self.db:
            self.db.close()

    def make_member_dao(self, make_member):
        self.connect()
        cur = self.db.cursor()
        
        data = (make_member.username, make_member.email)

        # SELECT로 중복 확인 아무것도 나오면 안됨
        sql = "SELECT * FROM member WHERE (username = %s) OR (email = %s)"

        cur.execute(sql, data)
        
        result = cur.fetchone()

        if result is not None:
            cur.close()
            self.disconnect()
            return True
        
        # 회원가입으로 덮어씀
        sql = "INSERT INTO member(username, password, name, email) VALUES (%s, %s, %s, %s)"
        data = (make_member.username, make_member.password, make_member.name, make_member.email)

        cur.execute(sql,data)

        self.db.commit()
        cur.close()
        self.disconnect()
    

    def login_result(self, mem):
        self.connect()
        cur = self.db.cursor()
        data = (mem.username, mem.password)

        sql = "SELECT id FROM member WHERE (username = %s) AND (password = %s)"

        cur.execute(sql, data)

        result = cur.fetchone()

        if result is None:
            cur.close()
            self.disconnect()
            return None
        
        self.db.commit()
        cur.close()
        self.disconnect()
        self.id = result[0]
        return self.id
    
    def product_list_dao(self):
        self.connect()
        cur = self.db.cursor()

        sql = "SELECT id, name, price, stock FROM product"
        cur.execute(sql)

        result = cur.fetchall()
        cur.close()
        self.disconnect()
        return result
    
    def find_product_dao(self, word):
        self.connect()
        cur = self.db.cursor()  
        
        sql = "SELECT id, name, price, stock FROM product WHERE name LIKE %s"
        data = (f"%{word}%",)

        cur.execute(sql, data)

        result = cur.fetchall()
        cur.close()
        self.disconnect()
        return result
    

    def order_dao(self, buy):
        self.connect()
        cur = self.db.cursor()

        # product에서 먼저 상품 아이디 가져오기, member에서 id는 이미 self.id로 저장함
        product_data = self.name
        sql_product_id = "SELECT id FROM product WHERE name = %s"
        sql_product_price = "SELECT price FROM product WHRE name = %s"

        sql_product_id = cur.execute(sql_product_id, product_data)
        sql_product_price = cur.execute(sql_product_price, product_data)

        # 헤더는 order_item 만들고 total_price 값 업데이트 해야 됨 디폴트 0임
        header_data = (self.id, 'ready')
        sql_order_header = "INSERT INTO order_header(member_id, status)  VALUES (%d, %s)"
        # cur.commit()


        # order_item 넣기
        sql_order_item = "INSERT INTO order_item(order_id, product_id, quantity, price) VALUES()"

        cur.execute(sql_order_header, header_data)

        sql_order_item = "INSERT INTO order_iem()"















class ServiceMenus:
    def __init__(self):
        self.dao = ServiceDAO()


    def create_id(self):
        while True:
            self.username = input("username(로그인 아이디): ")
            password = input("password :  ")

            tmp = ""
            for i in password: 
                tmp += chr(ord(i)+1)
            
            self.password = tmp

            self.member_name = input("이름(실명): ")
            self.email = input("email(중복X) : ")

            make_member = MEMBER(self.username, self.password, self.member_name, self.email)
            
            check = self.dao.make_member_dao(make_member)

            if check == True:
                print("중복 있음")
                continue
            else:
                print("회원가입 완료")
                break
    
    def login_check(self):
        while True:
            self.username = input("username(로그인 아이디): ")
            password = input("password :  ")

            tmp = ""
            for i in password: 
                tmp += chr(ord(i)+1)
            
            self.password = tmp

            check = MEMBER(self.username, self.password, "temp", "temp")
            
            self.id = self.dao.login_result(check)

            if self.id is None:
                print("로그인 실패")
                continue
            else:
                print("로그인 성공")
                login_menu = Login_Menu(self.id)
                login_menu.login_menu_run()
                break
    
    def product_list(self):
        products = self.dao.product_list_dao()
        
        print("==============================================================")
        print(f"{'상품번호':<5} | {'상품명':<10} | {'가격':<10} | {'재고':<5}")
        print("==============================================================")

        
        if not products:
            print("등록된 상품이 없습니다.")
        else:
            for i in products:
                p_id = i[0]
                p_name = i[1]
                p_price = i[2]
                p_stock = i[3]

                if p_stock <= 0:
                    p_stock = "품절임"
                else:
                    p_stock = str(p_stock)

                print(f"{p_id:<5} | {p_name:<10} | {p_price:<10} | {p_stock:<5}")
        print("==============================================================")

    def find_product(self):
        word = input("찾고 싶은 물건 입력: ")
        products = self.dao.find_product_dao(word)

        print("==============================================================")
        print(f"{'상품번호':<5} | {'상품명':<10} | {'가격':<10} | {'재고':<5}")
        print("==============================================================")

        if not products:
            print("검색 결과 없습니다.")
        else:
            for i in products:
                p_id = i[0]
                p_name = i[1]
                p_price = i[2]
                p_stock = i[3]

                if p_stock <= 0:
                    p_stock = "품절임"
                else:
                    p_stock = str(p_stock)

                print(f"{p_id:<5} | {p_name:<10} | {p_price:<10} | {p_stock:<5}")
        print("==============================================================")

    def order(self):
        while True:
            self.name = input("상품의 정확한 이름/ 그만 주문(0): ")

            if self.name == "0":
                print("메뉴로 돌아감")
                return
            
            self.num = input("상품의 개수: ")
            buy = PRODUCT(self.name, self.num)

            result = self.dao.order_dao(buy)
        







class Login_Menu(ServiceMenus):
    def __init__(self, id=None):
        super().__init__()
        self.id = id

    def login_menu_run(self):
        while True:
            try:
                print()
                print("==========================")
                print("    메인메뉴")
                print("==========================")
                print("1. 상품 목록 조회")
                print("2. 상품 검색")
                print("3. 주문하기")
                print("4. 주문 내역 조회")
                print("5. 로그아웃")
                print("0. 프로그램 종료")
                print("==========================")
                menu = int(input("메뉴 번호를 선택하세요: "))

                if menu == 1:
                    print("상품 목록 조회")
                    self.product_list()
                elif menu == 2:
                    print("상품검색")
                    self.service.find_product()
                elif menu == 3:
                    print("주문하기")
                    self.service.order() # self.id
                elif menu == 4:
                    print("주문 내역 조회")
                    self.service.watch_order() # self.id
                elif menu == 5:
                    print("로그아웃")
                    return 
                elif menu == 0:
                    print("종료")
                    exit()
                else:
                    print("메뉴는 1부터 0까지 입력해주세요")
            except Exception as e:
                print("오류: ", e)
                print("다시 입력하세요")

    


class First_Menu:
    def __init__(self):
        self.service = ServiceMenus()

    def run(self):
        while True:
            try:
                print()
                print("==========================")
                print("    온라인 스토어")
                print("==========================")
                print("1. 회원가입")
                print("2. 로그인")
                print("0. 프로그램 종료")
                print("==========================")
                menu = int(input("메뉴 번호를 선택하세요: "))

                if menu == 1:
                    print("회원가입합니다.")
                    self.service.create_id()

                elif menu == 2:
                    print("로그인합니다.")
                    self.service.login_check()
                    
                elif menu == 0:
                    print("종료")
                    exit()
                else:
                    print("메뉴는 1부터 0까지 입력해주세요")
            except Exception as e:
                print("오류: ", e)
                print("다시 입력하세요")
                


menu = First_Menu()
menu.run()
