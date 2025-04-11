from services.db.services.admin_service import AdminServiceDB


admin = AdminServiceDB()

def create_operator():
    admin.create_operator(
        tg_id=int(input("Введите тг ID оператора: ")),
        username= input("Введите @username оператора: "),
        fullname=input("Введиет полное имя оператора: "),
        group_id=int(input("Введите ID группы для оператора: "))
    )


try:
    create_operator()
except:
    print("Что-то неправильно введено. Заново.")
    create_operator()