import React from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { useAuthStore } from '../store/authStore';
import { 
  User, Shield, LogOut, Globe, Bell, 
  ChevronRight, TrendingUp, Zap, Sparkles 
} from 'lucide-react-native';

function SettingItem({ icon: Icon, label, value, onPress, danger }) {
  return (
    <TouchableOpacity 
        style={styles.settingItem} 
        onPress={onPress}
        activeOpacity={0.7}
    >
      <View style={[styles.settingIcon, { backgroundColor: danger ? '#ef444415' : '#ffffff05' }]}>
        <Icon color={danger ? '#ef4444' : '#a3a3a3'} size={20} />
      </View>
      <Text style={[styles.settingLabel, danger && { color: '#ef4444' }]}>{label}</Text>
      {value && <Text style={styles.settingValue}>{value}</Text>}
      <ChevronRight color="#404040" size={18} />
    </TouchableOpacity>
  );
}

export default function ProfileScreen() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    Alert.alert(
      "Sign Out",
      "Are you sure you want to log out of HunterOS?",
      [
        { text: "Cancel", style: "cancel" },
        { text: "Log Out", style: "destructive", onPress: logout }
      ]
    );
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.profileHeader}>
          <View style={styles.avatarLarge}>
            <Text style={styles.avatarTextLarge}>{user?.full_name?.[0] || 'H'}</Text>
          </View>
          <Text style={styles.profileName}>{user?.full_name || 'Hunter User'}</Text>
          <Text style={styles.profileEmail}>{user?.email || 'hunter@example.com'}</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Career Persona</Text>
          <View style={styles.personaCard}>
             <View style={styles.personaHeader}>
                <Sparkles color="#7c3aed" size={16} />
                <Text style={styles.personaTitle}>AI Professional Identity</Text>
             </View>
             <Text style={styles.personaSummary}>
                {user?.identity_data?.summary || "Senior Engineer specializing in high-scale distributed systems and AI integration."}
             </Text>
             <View style={styles.skillsRow}>
                {(user?.identity_data?.skills || ["Python", "React", "AWS", "Docker"]).map((skill, idx) => (
                  <View key={idx} style={styles.skillTag}>
                    <Text style={styles.skillTagText}>{skill}</Text>
                  </View>
                ))}
             </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <View style={styles.card}>
            <SettingItem icon={User} label="Personal Information" />
            <SettingItem icon={Shield} label="Privacy & Security" />
            <SettingItem icon={Bell} label="Notifications" value="Enabled" />
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Agent Configuration</Text>
          <View style={styles.card}>
            <SettingItem icon={Globe} label="API Endpoint" value="localhost:8000" />
            <SettingItem icon={TrendingUp} label="Match Threshold" value="80%" />
          </View>
        </View>

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <LogOut color="#ef4444" size={20} />
          <Text style={styles.logoutText}>Sign Out</Text>
        </TouchableOpacity>

        <Text style={styles.versionText}>HunterOS Mobile v1.0.0 (Alpha)</Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  scrollContent: {
    padding: 24,
    paddingTop: 60,
  },
  profileHeader: {
    alignItems: 'center',
    marginBottom: 40,
  },
  avatarLarge: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: '#7c3aed',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    shadowColor: '#7c3aed',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 10,
  },
  avatarTextLarge: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
  },
  profileName: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
  },
  profileEmail: {
    color: '#737373',
    fontSize: 14,
    marginTop: 4,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    color: '#525252',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 1.5,
    marginBottom: 12,
    marginLeft: 4,
  },
  card: {
    backgroundColor: '#171717',
    borderRadius: 24,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#262626',
  },
  personaCard: {
    backgroundColor: '#7c3aed08',
    borderRadius: 24,
    padding: 20,
    borderWidth: 1,
    borderColor: '#7c3aed20',
  },
  personaHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  personaTitle: {
    color: '#a78bfa',
    fontSize: 13,
    fontWeight: 'bold',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  personaSummary: {
    color: '#d4d4d4',
    fontSize: 14,
    lineHeight: 22,
    marginBottom: 16,
  },
  skillsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  skillTag: {
    backgroundColor: '#171717',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#262626',
  },
  skillTagText: {
    color: '#a3a3a3',
    fontSize: 10,
    fontWeight: 'bold',
    textTransform: 'uppercase',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#262626',
  },
  settingIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  settingLabel: {
    flex: 1,
    color: '#d4d4d4',
    fontSize: 15,
    fontWeight: '500',
  },
  settingValue: {
    color: '#737373',
    fontSize: 13,
    marginRight: 8,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ef444410',
    height: 56,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#ef444420',
    gap: 8,
    marginBottom: 24,
  },
  logoutText: {
    color: '#ef4444',
    fontSize: 16,
    fontWeight: '700',
  },
  versionText: {
    color: '#404040',
    fontSize: 11,
    textAlign: 'center',
    fontWeight: '500',
  }
});
