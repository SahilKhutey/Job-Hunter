import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";

export const useAuth = () => {
  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);
};
