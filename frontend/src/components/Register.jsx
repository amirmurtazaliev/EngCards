import { useState } from "react";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!name || !email || !password) {
      setError("Пожалуйста, заполните все поля");
      return;
    }

    if (!email.includes("@")) {
      setError("Введите корректный email");
      return;
    }

    if (password.length < 6) {
      setError("Слишком короткий пароль");
      return;
    }
    setIsLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/user/register",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ name, email, password }),
        },
      );

      console.log("выполнена регистрация:", { name, email, password });
    } catch (err) {
      setError("Ошибка при входе. Попробуйте снова.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="register-window">
      <form onSubmit={handleSubmit} className="register-form">
        <h2>Вход в аккаунт</h2>

        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="name">Your name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Amir"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="example@mail.com"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Пароль:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            disabled={isLoading}
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? "регистрация..." : "Register"}
        </button>
      </form>
    </div>
  );
};

export default Register;
