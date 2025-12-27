import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import { UserButton } from "@clerk/clerk-react";
import "./Layout.css";

export function Layout() {
  const location = useLocation();

  const isActive = (path) =>
    location.pathname === path
      ? "app-nav-link app-nav-link-active"
      : "app-nav-link";

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <div className="app-logo">
          <span className="app-logo-dot" />
          <span className="app-logo-text">CodeGuard AI</span>
        </div>

        <nav className="app-nav">
          <Link to="/" className={isActive("/")}>
            Retos
          </Link>
          <Link to="/history" className={isActive("/history")}>
            Historial
          </Link>
        </nav>

        <div className="app-sidebar-footer">
          <p>Sesión segura con Clerk</p>
        </div>
      </aside>

      <main className="app-main">
        <header className="app-header">
          <div className="app-header-left">
            <h1>CodeGuard – Reto diario</h1>
            <p>
              Practica lógica y lectura de código con preguntas técnicas
              generadas por IA, adaptadas a tu nivel.
            </p>
          </div>

          <div className="app-header-right">
            <div className="app-header-badge">
              <span className="app-header-badge-top">Modo seguro</span>
              <span className="app-header-badge-bottom">
                Autenticado con Clerk
              </span>
            </div>

            <UserButton
              afterSignOutUrl="/sign-in"
              appearance={{
                elements: {
                  rootBox: "clerk-userbutton-root",
                  avatarBox: "clerk-userbutton-avatar",
                },
              }}
            />
          </div>
        </header>

        <section className="app-content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
