import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

const Header = () => {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);

  const handleOpenLogin = () => {
    setIsLoginOpen(true);
  };

  const handleCloseLogin = () => {
    setIsLoginOpen(false);
  };

  const handleOpenRegister = () => {
    setIsRegisterOpen(true);
  };

  const handleCloseRegister = () => {
    setIsRegisterOpen(false);
  };

  return (
    <header className="header">
      <div className="container header-inner">
        <h1 className="logo">Boardly</h1>
        <nav className="nav">
          <a href="#">Home</a>
          <a href="#">About</a>
          <a href="#">Support</a>
        </nav>

        <button onClick={handleOpenLogin}>Sign In</button>
        {isLoginOpen && (
          <div className="modal-overlay" onClick={handleCloseLogin}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="close-btn" onClick={handleCloseLogin}>
                ×
              </button>
              <Login />
            </div>
          </div>
        )}

        <button onClick={handleOpenRegister}>Register</button>
        {isRegisterOpen && (
          <div className="modal-overlay" onClick={handleCloseRegister}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="close-btn" onClick={handleCloseRegister}>
                ×
              </button>
              <Register />
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
