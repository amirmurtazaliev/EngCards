import { useEffect, useMemo, useState } from "react";
import "./App.css";

const AUTH_API = "http://localhost:8000/api/v1/user";
const VERIFICATION_API = "http://localhost:8000/api/v1/user";
const CARD_API = "http://localhost:8010/api/v1/cards";
const LOCAL_CARDS_KEY = "engcards.cards";

const demoCards = [
  { id: "demo-1", english_word: "confidence", russian_word: "уверенность" },
  { id: "demo-2", english_word: "journey", russian_word: "путешествие" },
  { id: "demo-3", english_word: "practice", russian_word: "практика" },
];

const features = [
  {
    title: "Карточки без лишнего шума",
    text: "В личном кабинете остаются только ваши слова: английская сторона, русский перевод и быстрые действия.",
  },
  {
    title: "Тренировка кликом",
    text: "Нажимайте на карточку, чтобы перевернуть ее и проверить перевод. Открытие работает прямо на фронтенде.",
  },
  {
    title: "Свой словарь каждый день",
    text: "Добавляйте новые слова после уроков, фильмов или книг и возвращайтесь к ним в удобном интерфейсе.",
  },
];

function readLocalCards() {
  try {
    const savedCards = JSON.parse(localStorage.getItem(LOCAL_CARDS_KEY));
    return Array.isArray(savedCards) && savedCards.length > 0
      ? savedCards
      : demoCards;
  } catch {
    return demoCards;
  }
}

function App() {
  const [view, setView] = useState("landing");
  const [authMode, setAuthMode] = useState(null);
  const [user, setUser] = useState(null);
  const [cards, setCards] = useState(readLocalCards);
  const [cardError, setCardError] = useState("");
  const [isCardsLoading, setIsCardsLoading] = useState(false);

  const isAuthenticated = Boolean(user);

  useEffect(() => {
    localStorage.setItem(LOCAL_CARDS_KEY, JSON.stringify(cards));
  }, [cards]);

  useEffect(() => {
    if (!isAuthenticated) {
      return;
    }

    const loadCards = async () => {
      setIsCardsLoading(true);
      setCardError("");

      try {
        const response = await fetch(CARD_API, { credentials: "include" });

        if (!response.ok) {
          throw new Error("Card service is unavailable");
        }

        const payload = await response.json();
        setCards(payload.cards ?? []);
      } catch {
        setCardError(
          "Cardservice пока недоступен, поэтому показаны карточки из браузера.",
        );
      } finally {
        setIsCardsLoading(false);
      }
    };

    loadCards();
  }, [isAuthenticated]);

  const stats = useMemo(
    () => [
      { value: cards.length, label: "карточек в кабинете" },
      { value: "2", label: "языка на каждой карточке" },
      { value: "1 click", label: "чтобы проверить перевод" },
    ],
    [cards.length],
  );

  const handleAuthenticated = (profile) => {
    setUser(profile);
    setView("dashboard");
    setAuthMode(null);
  };

  const handleLogout = () => {
    setUser(null);
    setView("landing");
  };

  const handleCreateCard = async (newCard) => {
    setCardError("");
    const optimisticCard = { id: crypto.randomUUID(), ...newCard };

    try {
      const response = await fetch(CARD_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(newCard),
      });

      if (!response.ok) {
        throw new Error("Unable to save card");
      }

      const payload = await response.json();
      setCards((currentCards) => [payload.card, ...currentCards]);
    } catch {
      setCards((currentCards) => [optimisticCard, ...currentCards]);
      setCardError(
        "Не получилось сохранить карточку на сервере. Она временно сохранена в браузере.",
      );
    }
  };

  const handleDeleteCard = async (cardId) => {
    const previousCards = cards;
    setCards((currentCards) =>
      currentCards.filter((card) => card.id !== cardId),
    );

    if (String(cardId).startsWith("demo-")) {
      return;
    }

    try {
      const response = await fetch(`${CARD_API}/${cardId}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Unable to delete card");
      }
    } catch {
      setCards(previousCards);
      setCardError(
        "Не получилось удалить карточку на сервере. Попробуйте еще раз.",
      );
    }
  };

  return (
    <div className="app">
      <Header
        isAuthenticated={isAuthenticated}
        onAuthOpen={setAuthMode}
        onHome={() => setView("landing")}
        onDashboard={() => setView("dashboard")}
        onLogout={handleLogout}
      />

      {view === "dashboard" && isAuthenticated ? (
        <Dashboard
          cards={cards}
          user={user}
          error={cardError}
          isLoading={isCardsLoading}
          onCreateCard={handleCreateCard}
          onDeleteCard={handleDeleteCard}
        />
      ) : (
        <Landing stats={stats} onStart={() => setAuthMode("register")} />
      )}

      <Footer />

      {authMode && (
        <AuthModal
          mode={authMode}
          onClose={() => setAuthMode(null)}
          onModeChange={setAuthMode}
          onAuthenticated={handleAuthenticated}
        />
      )}
    </div>
  );
}

function Header({
  isAuthenticated,
  onAuthOpen,
  onHome,
  onDashboard,
  onLogout,
}) {
  return (
    <header className="site-header">
      <div className="shell header-inner">
        <button
          className="brand"
          onClick={onHome}
          type="button"
          aria-label="EngCards home"
        >
          <span className="brand-mark">EC</span>
          <span>EngCards</span>
        </button>

        <nav className="nav" aria-label="Main navigation">
          <a href="#about">О проекте</a>
          <a href="#how-it-works">Как работает</a>
          <a href="#footer">Контакты</a>
        </nav>

        <div className="header-actions">
          {isAuthenticated ? (
            <>
              <button
                className="primary-button"
                onClick={onLogout}
                type="button"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <button
                className="ghost-button"
                onClick={() => onAuthOpen("login")}
                type="button"
              >
                Sign In
              </button>
              <button
                className="primary-button"
                onClick={() => onAuthOpen("register")}
                type="button"
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

function Landing({ stats, onStart }) {
  return (
    <main>
      <section className="hero shell" id="about">
        <div className="hero-copy">
          <p className="eyebrow">English vocabulary trainer</p>
          <h1>
            Учите английские слова на карточках, которые всегда под рукой.
          </h1>
          <p className="hero-text">
            EngCards — это приложение для создания личного словаря. Вы
            добавляете слово на английском, указываете перевод на русском и
            тренируетесь через понятные flip-карточки: сначала видите английскую
            сторону, а после клика проверяете себя.
          </p>
          <div className="hero-actions">
            <button
              className="primary-button large"
              onClick={onStart}
              type="button"
            >
              Создать кабинет
            </button>
            <a className="secondary-link" href="#how-it-works">
              Посмотреть возможности
            </a>
          </div>
          <div className="stats-grid" aria-label="Project stats">
            {stats.map((item) => (
              <div className="stat-card" key={item.label}>
                <strong>{item.value}</strong>
                <span>{item.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-art" aria-hidden="true">
          <div className="floating-card card-one">
            <span>discover</span>
            <strong>открывать</strong>
          </div>
          <div className="floating-card card-two">
            <span>remember</span>
            <strong>запоминать</strong>
          </div>
          <div className="phone-mockup">
            <div className="phone-top" />
            <div className="lesson-card">
              <span>English</span>
              <strong>achievement</strong>
              <small>Нажми, чтобы увидеть перевод</small>
            </div>
            <div className="mini-row">
              <span /> <span /> <span />
            </div>
          </div>
        </div>
      </section>

      <section className="feature-section shell" id="how-it-works">
        <div className="section-heading">
          <p className="eyebrow">Как устроено приложение</p>
          <h2>
            От лендинга до личного кабинета — все под один учебный сценарий.
          </h2>
        </div>
        <div className="feature-grid">
          {features.map((feature, index) => (
            <article className="feature-card" key={feature.title}>
              <div className="feature-icon">0{index + 1}</div>
              <h3>{feature.title}</h3>
              <p>{feature.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="showcase shell">
        <div className="showcase-panel">
          <div>
            <p className="eyebrow">Backend ready</p>
            <h2>Cardservice хранит карточки отдельно от authservice.</h2>
            <p>
              Для каждой карточки сохраняется английское слово и русский
              перевод. Открытие и переворот карточки не требуют запроса к
              серверу — интерфейс делает это мгновенно.
            </p>
          </div>
          <div className="diagram" aria-hidden="true">
            <span>Создавай</span>
            <b />
            <span>Учи</span>
            <b />
            <span>Проверяй</span>
          </div>
        </div>
      </section>
    </main>
  );
}

function AuthModal({ mode, onClose, onModeChange, onAuthenticated }) {
  return (
    <div className="modal-overlay" onClick={onClose} role="presentation">
      <div
        className="modal-content"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          className="close-btn"
          onClick={onClose}
          type="button"
          aria-label="Close modal"
        >
          ×
        </button>
        <AuthForm
          mode={mode}
          onModeChange={onModeChange}
          onAuthenticated={onAuthenticated}
          onClose={onClose}
        />
      </div>
    </div>
  );
}

function AuthForm({ mode, onModeChange, onAuthenticated, onClose }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [verificationCode, setVerificationCode] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isVerificationStep, setIsVerificationStep] = useState(false);
  const [tempUserData, setTempUserData] = useState(null);
  const isRegister = mode === "register";

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if ((isRegister && !name.trim()) || !email.trim() || !password) {
      setError("Пожалуйста, заполните все поля.");
      return;
    }

    if (!email.includes("@")) {
      setError("Введите корректный email.");
      return;
    }

    if (password.length < 6) {
      setError("Пароль должен быть не короче 6 символов.");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(
        `${AUTH_API}/${isRegister ? "register" : "login"}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify(
            isRegister ? { name, email, password } : { email, password },
          ),
        },
      );

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || "Не удалось войти в аккаунт.");
      }

      if (isRegister) {
        // После успешной регистрации отправляем код подтверждения
        await sendVerificationCode(email);

        // Сохраняем данные пользователя для последующей авторизации
        setTempUserData({ name: name || email.split("@")[0], email });
        setIsVerificationStep(true);
      } else {
        // Для логина сразу авторизуем
        onAuthenticated({ name: name || email.split("@")[0], email });
        onClose();
      }
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const sendVerificationCode = async (emailToVerify) => {
    try {
      const response = await fetch(
        `${VERIFICATION_API}/send_verification_code`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ email: emailToVerify }),
        },
      );

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(
          payload.detail || "Не удалось отправить код подтверждения.",
        );
      }

      return await response.json();
    } catch (error) {
      throw new Error(
        error.message || "Ошибка при отправке кода подтверждения",
      );
    }
  };

  const handleVerifyCode = async (event) => {
    event.preventDefault();
    setError("");

    if (!verificationCode || verificationCode.length !== 4) {
      setError("Введите корректный код подтверждения (4 цифр).");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${VERIFICATION_API}/verify_email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email: tempUserData.email,
          code: parseInt(verificationCode, 10),
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || "Неверный код подтверждения.");
      }

      // Код подтвержден успешно - авторизуем пользователя
      onAuthenticated(tempUserData);
      onClose();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendCode = async () => {
    setError("");
    setIsLoading(true);

    try {
      await sendVerificationCode(tempUserData.email);
      setError("Код подтверждения отправлен повторно. Проверьте вашу почту.");
      // Очищаем сообщение через 5 секунд
      setTimeout(() => {
        if (
          error ===
          "Код подтверждения отправлен повторно. Проверьте вашу почту."
        ) {
          setError("");
        }
      }, 5000);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToRegistration = () => {
    setIsVerificationStep(false);
    setVerificationCode("");
    setTempUserData(null);
    setError("");
  };

  // Если мы на этапе верификации, показываем форму ввода кода
  if (isVerificationStep) {
    return (
      <form className="auth-form" onSubmit={handleVerifyCode}>
        <p className="eyebrow">Подтверждение email</p>
        <h2>Введите код подтверждения</h2>
        <p className="form-hint">
          Мы отправили код подтверждения на ваш email:{" "}
          <strong>{tempUserData?.email}</strong>
          <br />
          Пожалуйста, проверьте почту и введите полученный код.
        </p>

        {error && <div className="error-message">{error}</div>}

        <label className="form-group" htmlFor="verification_code">
          Код подтверждения
          <input
            id="verification_code"
            type="text"
            value={verificationCode}
            onChange={(event) => setVerificationCode(event.target.value)}
            placeholder="1234"
            maxLength="4"
            disabled={isLoading}
            autoComplete="off"
          />
        </label>

        <button
          className="primary-button wide"
          type="submit"
          disabled={isLoading}
        >
          {isLoading ? "Проверяем..." : "Подтвердить email"}
        </button>

        <div className="verification-actions">
          <button
            className="text-button"
            type="button"
            onClick={handleResendCode}
            disabled={isLoading}
          >
            Отправить код повторно
          </button>

          <button
            className="text-button"
            type="button"
            onClick={handleBackToRegistration}
            disabled={isLoading}
          >
            ← Вернуться к регистрации
          </button>
        </div>
      </form>
    );
  }

  // Основная форма регистрации/логина
  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <p className="eyebrow">{isRegister ? "Новый аккаунт" : "Возвращение"}</p>
      <h2>{isRegister ? "Регистрация" : "Вход в кабинет"}</h2>
      <p className="form-hint">
        {isRegister
          ? "Создайте аккаунт и сразу перейдите в личный кабинет с карточками."
          : "Войдите, чтобы открыть сохраненные карточки пользователя."}
      </p>

      {error && <div className="error-message">{error}</div>}

      {isRegister && (
        <label className="form-group" htmlFor="name">
          Имя
          <input
            id="name"
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Amir"
            disabled={isLoading}
          />
        </label>
      )}

      <label className="form-group" htmlFor="email">
        Email
        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="example@mail.com"
          disabled={isLoading}
        />
      </label>

      <label className="form-group" htmlFor="password">
        Пароль
        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="••••••••"
          disabled={isLoading}
        />
      </label>

      <button
        className="primary-button wide"
        type="submit"
        disabled={isLoading}
      >
        {isLoading
          ? "Отправляем..."
          : isRegister
            ? "Зарегистрироваться"
            : "Войти"}
      </button>

      <button
        className="text-button"
        type="button"
        onClick={() => onModeChange(isRegister ? "login" : "register")}
      >
        {isRegister
          ? "Уже есть аккаунт? Войти"
          : "Нет аккаунта? Зарегистрироваться"}
      </button>
    </form>
  );
}

function Dashboard({
  cards,
  user,
  error,
  isLoading,
  onCreateCard,
  onDeleteCard,
}) {
  return (
    <main className="dashboard shell">
      <section className="dashboard-hero">
        <div>
          <p className="eyebrow">Личный кабинет</p>
          <h1>Привет, {user.name}! Ваши карточки уже здесь.</h1>
          <p>
            Добавляйте слова на английском и русском, удаляйте лишнее и
            открывайте перевод простым нажатием на карточку.
          </p>
        </div>
        <div className="dashboard-badge">
          <strong>{cards.length}</strong>
          <span>cards saved</span>
        </div>
      </section>

      <section className="workspace-grid">
        <CardCreateForm onCreateCard={onCreateCard} />
        <div className="cards-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Мой словарь</p>
              <h2>Карточки пользователя</h2>
            </div>
            {isLoading && <span className="loading-label">Загрузка...</span>}
          </div>

          {error && <div className="warning-message">{error}</div>}

          <div className="cards-grid">
            {cards.map((card) => (
              <FlipCard key={card.id} card={card} onDeleteCard={onDeleteCard} />
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

function CardCreateForm({ onCreateCard }) {
  const [englishWord, setEnglishWord] = useState("");
  const [russianWord, setRussianWord] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    setError("");

    if (!englishWord.trim() || !russianWord.trim()) {
      setError("Введите английское слово и русский перевод.");
      return;
    }

    onCreateCard({
      english_word: englishWord.trim(),
      russian_word: russianWord.trim(),
    });
    setEnglishWord("");
    setRussianWord("");
  };

  return (
    <form className="create-card-form" onSubmit={handleSubmit}>
      <p className="eyebrow">Новая карточка</p>
      <h2>Создать карточку</h2>
      <p>Заполните две стороны карточки: английское слово и русский перевод.</p>

      {error && <div className="error-message">{error}</div>}

      <label className="form-group" htmlFor="english_word">
        Слово на английском
        <input
          id="english_word"
          type="text"
          value={englishWord}
          onChange={(event) => setEnglishWord(event.target.value)}
          placeholder="inspiration"
        />
      </label>

      <label className="form-group" htmlFor="russian_word">
        Слово на русском
        <input
          id="russian_word"
          type="text"
          value={russianWord}
          onChange={(event) => setRussianWord(event.target.value)}
          placeholder="вдохновение"
        />
      </label>

      <button className="primary-button wide" type="submit">
        Добавить карточку
      </button>
    </form>
  );
}

function FlipCard({ card, onDeleteCard }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <article className="card-wrapper">
      <button
        className={`study-card ${isFlipped ? "is-flipped" : ""}`}
        onClick={() => setIsFlipped((currentValue) => !currentValue)}
        type="button"
        aria-label={`Открыть перевод слова ${card.english_word}`}
      >
        <span className="card-face card-front">
          <small>English</small>
          <strong>{card.english_word}</strong>
          <em>Нажмите, чтобы открыть перевод</em>
        </span>
        <span className="card-face card-back">
          <small>Русский</small>
          <strong>{card.russian_word}</strong>
          <em>Нажмите, чтобы вернуться</em>
        </span>
      </button>
      <button
        className="delete-card"
        type="button"
        onClick={() => onDeleteCard(card.id)}
      >
        Удалить
      </button>
    </article>
  );
}

function Footer() {
  return (
    <footer className="footer" id="footer">
      <div className="shell footer-inner">
        <div>
          <strong>EngCards</strong>
          <p>Персональный тренажер английских слов.</p>
        </div>
        <a href="mailto:petprojectauth@gmail.com">petprojectauth@gmail.com</a>
      </div>
    </footer>
  );
}

export default App;
