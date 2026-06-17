import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

function ProtectedRoute({ children }) {
    const { isAuthenticated, loading } = useAuth();

    if (loading) return null;
    if (!isAuthenticated) return <Navigate to="/login" replace />;
    return children;
}

function HabitsPage() { return <div>Habits</div>; }
function StatsPage() { return <div>Stats</div>; }

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/habits" replace />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/habits" element={
                    <ProtectedRoute><HabitsPage /></ProtectedRoute>
                } />
                <Route path="/stats" element={
                    <ProtectedRoute><StatsPage /></ProtectedRoute>
                } />
            </Routes>
        </BrowserRouter>
    );
}
