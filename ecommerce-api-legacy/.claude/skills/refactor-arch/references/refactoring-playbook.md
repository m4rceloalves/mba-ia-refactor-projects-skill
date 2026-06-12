# Refactoring Playbook

Apply the smallest transformation that removes the smell while preserving behavior.

## 1. Extract Config

Before:
```python
app.config["SECRET_KEY"] = "secret"
```
After:
```python
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-secret")
```

## 2. Parameterize SQL

Before:
```python
cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
```
After:
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

## 3. Split Route From Controller

Before:
```javascript
app.post('/checkout', (req, res) => { /* all logic */ });
```
After:
```javascript
router.post('/checkout', checkoutController.checkout);
```

## 4. Move Domain Logic To Services

Before:
```python
if priority < 1 or priority > 5: return error
```
After:
```python
payload = task_service.validate_payload(data)
```

## 5. Introduce Repository/Model Functions

Before:
```javascript
db.get("SELECT * FROM courses WHERE id = ?", [id], cb)
```
After:
```javascript
const course = await courseModel.findActiveById(id);
```

## 6. Centralize Error Handling

Before:
```python
except Exception as e:
    return jsonify({"error": str(e)}), 500
```
After:
```python
raise AppError("Erro interno", 500)
```

## 7. Secure Passwords

Before:
```python
hashlib.md5(password.encode()).hexdigest()
```
After:
```python
generate_password_hash(password)
```

## 8. Remove Sensitive Serialization

Before:
```python
return {"email": self.email, "password": self.password}
```
After:
```python
return {"email": self.email}
```

## 9. Replace N+1 Queries

Before:
```python
for user in users:
    Task.query.filter_by(user_id=user.id).all()
```
After:
```python
rows = db.session.query(User, func.count(Task.id)).outerjoin(Task).group_by(User.id)
```

## 10. Replace Deprecated APIs

Before:
```python
User.query.get(user_id)
```
After:
```python
db.session.get(User, user_id)
```
