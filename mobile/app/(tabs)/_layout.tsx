import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

export default function TabsLayout() {
    return (
        <Tabs
            screenOptions={{
                headerShown: false,
                tabBarStyle: { 
                    backgroundColor: "#0A0A0A",
                    borderTopWidth: 1,
                    borderTopColor: "rgba(255,255,255,0.05)",
                    height: 60,
                    paddingBottom: 10
                },
                tabBarActiveTintColor: "#6366F1",
                tabBarInactiveTintColor: "#71717A",
            }}
        >
            <Tabs.Screen
                name="dashboard"
                options={{
                    title: "Home",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="home-outline" size={22} color={color} />
                    ),
                }}
            />
            <Tabs.Screen
                name="jobs"
                options={{
                    title: "Jobs",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="briefcase-outline" size={22} color={color} />
                    ),
                }}
            />
            <Tabs.Screen
                name="analytics"
                options={{
                    title: "Stats",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="bar-chart-outline" size={22} color={color} />
                    ),
                }}
            />
            <Tabs.Screen
                name="profile"
                options={{
                    title: "Profile",
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="person-outline" size={22} color={color} />
                    ),
                }}
            />
        </Tabs>
    );
}
