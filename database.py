import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data.db')

    def __query(self, query, commit=True):
        """Создает запрос к базе данных. commit = False не сохраняет таблицу"""
        cursor = self.connection.cursor()
        record = cursor.execute(query).fetchall()
        if commit:
            self.connection.commit()
        cursor.close()
        return record

    def add_user(self, user_id):
        """Добавляет пользователя в базу данных"""
        query = f"INSERT INTO users (id, first_name, second_name, phone) VALUES ({user_id}, Null, Null, Null);"
        self.__query(query)

    def user_exist(self, user_id):
        """Проверяет существование пользователя в базе данных"""
        query = f"SELECT * FROM users WHERE id = {user_id};"
        record = self.__query(query, commit=False)
        if record == []:
            return False
        return True

    def ticket_exist(self, user_id):
        """Проверяет существование талона пользователя в базе данных"""
        query = f"SELECT * FROM ticket WHERE user_id = {user_id};"
        record = self.__query(query, commit=False)
        if record == []:
            return False
        return True

    def set_first_name_for_user(self, user_id, first_name):
        query = f"UPDATE users SET first_name = '{first_name}' WHERE id = {user_id};"
        self.__query(query)

    def set_second_name_for_user(self, user_id, second_name):
        query = f"UPDATE users SET second_name = '{second_name}' WHERE id = {user_id};"
        self.__query(query)

    def set_phone_for_user(self, user_id, phone):
        query = f"UPDATE users SET phone = {phone} WHERE id = {user_id};"
        self.__query(query)

    def get_info_about_user(self, user_id):
        query = f"SELECT first_name, second_name, phone FROM users WHERE id = {user_id};"
        record = self.__query(query, commit=False)[0]
        answer = {"first_name": record[1],
                  "second_name": record[2],
                  "phone": record[3]}
        return answer

    def clear_user_data(self, user_id):
        query = f"UPDATE users SET first_name = Null, second_name = Null, phone = Null WHERE id = {user_id};"
        self.__query(query)

    def add_ticket(self, user_id):
        query = f"INSERT INTO ticket (user_id) VALUES ({user_id})"
        self.__query(query)

    def set_service_for_user(self, user_id, service_id):
        query = f"UPDATE ticket SET serv_id = {service_id} WHERE user_id = {user_id}"
        if not self.ticket_exist(user_id):
            self.add_ticket(user_id)
        self.__query(query)

    def set_doctor_for_user(self, user_id, doctor_id):
        query = f"UPDATE ticket SET doc_id = {doctor_id} WHERE user_id = {user_id}"
        self.__query(query)

    def get_all_doctors_for_service(self, service_id):
        query = f"SELECT id, name FROM doctors WHERE serv_id = {service_id}"
        return self.__query(query, commit=False)

    def get_all_services(self):
        query = f"SELECT id, name FROM service"
        return self.__query(query, commit=False)

    def get_all_tickets(self):
        query = f"SELECT user_id, id FROM ticket"
        return self.__query(query, commit=False)

    def get_ticket(self, user_id):
        query = f"SELECT doc_id, serv_id FROM ticket WHERE user_id = {user_id}"
        record = self.__query(query, commit=False)
        user = f"SELECT first_name, second_name FROM users WHERE id = {user_id}"
        doctor = f"SELECT name FROM doctors WHERE id = {record[0][0]}"
        service = f"SELECT name FROM service WHERE id = {record[0][1]}"
        price = f"SELECT price FROM service WHERE id = {record[0][1]}"
        room = f"SELECT room FROM doctors WHERE id = {record[0][0]}"
        user = " ".join(self.__query(user, commit=False)[0])
        doctor = self.__query(doctor, commit=False)[0][0]
        service = self.__query(service, commit=False)[0][0]
        price = self.__query(price, commit=False)[0][0]
        room = self.__query(room, commit=False)[0][0]
        return {"user": user, "doctor": doctor, "service": service, "price": price, "room": room}



