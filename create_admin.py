from services.db.services.admin_service import AdminServiceDB


admin = AdminServiceDB()

def create_operator():
    admin.create_admin(
        tg_id=int(input("Введите тг ID администратора: ")),
        username= input("Введите @username администратора: "),
        fullname=input("Введиет полное имя администратора: "),
    )

try:
    create_operator()
except:
    print("Что-то неправильно введено. Заново.")
    create_operator()