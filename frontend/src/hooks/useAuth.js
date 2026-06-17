import { useState, useEffect } from "react";
import { login as apiLogin, getMe } from "../api/auth";

export function useAuth() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(() => !!localStorage.getItem("token"));

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) return;
        getMe()
            .then(setUser)
            .catch(() => localStorage.removeItem("token"))
            .finally(() => setLoading(false));
    }, []);

    function login(credentials) {
        return apiLogin(credentials).then(({ access_token }) => {
            localStorage.setItem("token", access_token);
            return getMe().then(setUser);
        });
    }

    function logout() {
        localStorage.removeItem("token");
        setUser(null);
    }

    return { user, loading, login, logout, isAuthenticated: !!user };
}