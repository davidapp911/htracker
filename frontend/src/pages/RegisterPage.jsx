import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";

export default function RegisterPage() {
    const [form, setForm] = useState( { email: "", username: "", password: ""} );
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    function handleChange(e) {
        setForm({...form, [e.target.name]: e.target.value });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await register(form);
            navigate("/login");
        } catch (err) {
            setError(err.response?.data?.detail ?? "Register Failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-gray-700 p-8 rounded-xl w-full max-w-sm">
                <h1 className="text-white text-2xl font-semibold mb-6">Register Form</h1>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <input
                        name="email"
                        type="email"
                        placeholder="email"
                        value={form.email}
                        onChange={handleChange}
                        className="bg-gray-800 text-white rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        name="username"
                        type="text"
                        placeholder="username"
                        value={form.username}
                        onChange={handleChange}
                        className="bg-gray-800 text-white rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                        name="password"
                        type="password"
                        placeholder="password"
                        value={form.password}
                        onChange={handleChange}
                        className="bg-gray-800 text-white rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button type="submit" disabled={loading} className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg px-4 py-2 font-medium transition-colors">
                        {loading ? "Registering..." : "Register"}
                    </button>
                </form>
            </div>
        </div>
    );
}