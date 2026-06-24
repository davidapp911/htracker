import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Input from "../components/Input";
import Button from "../components/Button";

export default function LoginPage() {
    const [form, setForm] = useState({ username: "", password: "" });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const { login } = useAuth();
    const navigate = useNavigate();

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await login(form);
            navigate("/dashboard");
        } catch (err) {
            setError(err.response?.data?.detail ?? "Login failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center">
            <div className="bg-white dark:bg-gray-800 p-8 rounded-xl w-full max-w-sm shadow-sm dark:shadow-none">
                <h1 className="text-gray-900 dark:text-white text-2xl font-semibold mb-6">Log in</h1>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    {error && <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>}
                    <Input name="username" type="text" placeholder="username" value={form.username} onChange={handleChange} />
                    <Input name="password" type="password" placeholder="password" value={form.password} onChange={handleChange} />
                    <Button type="submit" disabled={loading} className="font-medium w-full py-2">
                        {loading ? "Logging in…" : "Log in"}
                    </Button>
                </form>
            </div>
        </div>
    );
}
