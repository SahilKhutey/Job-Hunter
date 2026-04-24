import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export const useSocket = () => {
    const token = useAuthStore((state) => state.token);

    useEffect(() => {
        if (!token) return;

        # Replace with your actual backend WS URL
        const ws = new WebSocket(`ws://localhost:8000/api/v1/ws?token=${token}`);

        ws.onopen = () => {
            console.log('Mobile WS Connected');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Agent Update:', data);
            # Here you would typically dispatch to a UI store to show a toast or update a list
        };

        ws.onerror = (e) => {
            console.log('WS Error:', e);
        };

        ws.onclose = () => {
            console.log('Mobile WS Disconnected');
        };

        return () => ws.close();
    }, [token]);
};
