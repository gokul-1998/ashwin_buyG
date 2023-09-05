


class User:
    def __init__(self,id, username, email, password,is_store_manager):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_store_manager = is_store_manager
        # 1 if the user is a store manager, 0 otherwise

    def __repr__(self):
        return '<User %r>' % self.username

admin=User(1,'admin','admin@admin.com','admin',1)
u1=User(2,'user1','user1@admin.com','user1',0)
u2=User(3,'user2','user2@admin.com','user2',0)
u3=User(4,'user3','user3@admin.com','user3',0)

print(admin.username)
print(u1.email)
print(u2.password)
print(u3.is_store_manager)

class Section:
    def __init__(self,id, name):
        self.id = id
        self.name = name
        
s1=Section(1,'Fruits')
s2=Section(2,'Vegetables')
s3=Section(3,'stationery')
s4=Section(4,'clothes')

print(s1.name)
print(s2.id)
print(s3.name)
print(s4.id)

class Product:
    def __init__(self,id, name, price,expiry_date, quantity_available, section_id, description):
        self.id = id
        self.name = name
        self.price = price # rate per unit  (e.g. 1kg)
        self.expiry_date = expiry_date
        self.quantity_available = quantity_available
        self.section_id = section_id
        self.description = description

p1=Product(1,'apple',10,'2021-12-31',100,1,'red apple')
p2=Product(2,'banana',20,'2021-12-31',100,1,'yellow banana')
p3=Product(3,'potato',30,'2021-12-31',100,2,'brown potato')
p4=Product(4,'tomato',40,'2021-12-31',100,2,'red tomato')
p5=Product(5,'pen',50,'2021-12-31',100,3,'blue pen')
p6=Product(6,'pencil',60,'2021-12-31',100,3,'black pencil')
p7=Product(7,'shirt',70,'2021-12-31',100,4,'white shirt')
p8=Product(8,'pants',80,'2021-12-31',100,4,'black pants')

print(p1.name)
print(p2.id)
print(p3.price)
print(p4.expiry_date)
print(p5.quantity_available)
print(p6.section_id)
print(p7.description)

users=[admin,u1,u2,u3]
print(users)
