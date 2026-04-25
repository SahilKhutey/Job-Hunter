import React, { useEffect, useState } from 'react';
import { 
  StyleSheet, View, Text, ScrollView, TouchableOpacity, 
  RefreshControl, Dimensions 
} from 'react-native';
import { useAuthStore } from '../store/authStore';
import api from '../lib/api';
import { Send, CheckCircle, Calendar, Sparkles, TrendingUp } from 'lucide-react-native';

const { width } = Dimensions.get('window');

function StatCard({ icon: Icon, label, value, sub, color }) {
  return (
    <View style={[styles.statCard, { borderColor: color + '33' }]}>
      <View style={[styles.statIcon, { backgroundColor: color + '15' }]}>
        <Icon color={color} size={20} />
      </View>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={styles.statSub}>{sub}</Text>
    </View>
  );
}

export default function DashboardScreen() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const [stats, setStats] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      const res = await api.get('/dashboard/stats?profile_id=1'); // Using default for demo
      setStats(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    fetchStats().finally(() => setRefreshing(false));
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView 
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#7c3aed" />}
      >
        <View style={styles.header}>
          <View>
            <View style={styles.liveIndicator}>
                <View style={styles.pulseDot} />
                <Text style={styles.liveText}>SYSTEM LIVE</Text>
            </View>
            <Text style={styles.greeting}>Good morning,</Text>
            <Text style={styles.name}>{user?.full_name?.split(' ')[0] || 'Hunter'}</Text>
          </View>
          <TouchableOpacity style={styles.profileButton} onPress={() => navigation.navigate('Profile')}>
            <View style={styles.avatar}>
               <Text style={styles.avatarText}>{user?.full_name?.[0] || 'H'}</Text>
            </View>
          </TouchableOpacity>
        </View>


        <View style={styles.strengthCard}>
            <View style={styles.strengthHeader}>
                <Text style={styles.strengthLabel}>Pipeline Strength</Text>
                <Text style={styles.strengthValue}>84%</Text>
            </View>
            <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: '84%' }]} />
            </View>
            <Text style={styles.strengthNote}>Your agent is actively matching high-value roles.</Text>
        </View>

        <View style={styles.statsGrid}>
          <StatCard 
            icon={Send} 
            label="Applications" 
            value={stats?.total_applications || 0} 
            sub="Active submission" 
            color="#8b5cf6" 
          />
          <StatCard 
            icon={CheckCircle} 
            label="Responses" 
            value={stats?.responses || 0} 
            sub={`${stats?.response_rate || 0}% rate`} 
            color="#10b981" 
          />
          <StatCard 
            icon={Calendar} 
            label="Interviews" 
            value={stats?.interviews || 0} 
            sub="Next: Tuesday" 
            color="#0ea5e9" 
          />
          <StatCard 
            icon={Sparkles} 
            label="AI Matches" 
            value={stats?.ai_matches_above_threshold || 0} 
            sub="High Precision" 
            color="#f59e0b" 
          />
        </View>

        <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recent Activity</Text>
            <TouchableOpacity>
                <Text style={styles.sectionLink}>View All</Text>
            </TouchableOpacity>
        </View>

        <View style={styles.activityCard}>
            <View style={styles.activityItem}>
                <View style={styles.activityIcon}>
                    <TrendingUp color="#8b5cf6" size={16} />
                </View>
                <View style={styles.activityText}>
                    <Text style={styles.activityTitle}>Match Score Updated</Text>
                    <Text style={styles.activityDesc}>Senior Product Designer at Google (92%)</Text>
                </View>
                <Text style={styles.activityTime}>2h ago</Text>
            </View>
            <View style={styles.activityItem}>
                <View style={styles.activityIcon}>
                    <Send color="#8b5cf6" size={16} />
                </View>
                <View style={styles.activityText}>
                    <Text style={styles.activityTitle}>Application Submitted</Text>
                    <Text style={styles.activityDesc}>Full Stack Engineer at Stripe</Text>
                </View>
                <Text style={styles.activityTime}>5h ago</Text>
            </View>
        </View>
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
    padding: 20,
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  greeting: {
    color: '#737373',
    fontSize: 16,
  },
  name: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  profileButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#171717',
    borderWidth: 1,
    borderColor: '#262626',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#7c3aed',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  strengthCard: {
    backgroundColor: '#171717',
    borderRadius: 24,
    padding: 20,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#262626',
  },
  strengthHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  strengthLabel: {
    color: '#a3a3a3',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  strengthValue: {
    color: '#a78bfa',
    fontSize: 14,
    fontWeight: 'bold',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#0a0a0a',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 12,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#7c3aed',
  },
  strengthNote: {
    color: '#525252',
    fontSize: 11,
    fontStyle: 'italic',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 24,
  },
  statCard: {
    width: (width - 52) / 2,
    backgroundColor: '#171717',
    borderRadius: 20,
    padding: 16,
    borderWidth: 1,
  },
  statIcon: {
    width: 32,
    height: 32,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  statValue: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  statLabel: {
    color: '#a3a3a3',
    fontSize: 12,
    fontWeight: '500',
  },
  statSub: {
    color: '#525252',
    fontSize: 10,
    marginTop: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  sectionLink: {
    color: '#a78bfa',
    fontSize: 13,
  },
  activityCard: {
    backgroundColor: '#171717',
    borderRadius: 24,
    padding: 12,
    borderWidth: 1,
    borderColor: '#262626',
  },
  activityItem: {
    flexDirection: 'row',
    padding: 12,
    alignItems: 'center',
  },
  activityIcon: {
    width: 32,
    height: 32,
    borderRadius: 10,
    backgroundColor: 'rgba(255,255,255,0.05)',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  activityText: {
    flex: 1,
  },
  activityTitle: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  activityDesc: {
    color: '#737373',
    fontSize: 12,
    marginTop: 2,
  },
  activityTime: {
    color: '#525252',
    fontSize: 10,
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    alignSelf: 'flex-start',
    marginBottom: 8,
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.2)',
  },
  pulseDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#10b981',
    marginRight: 6,
  },
  liveText: {
    color: '#10b981',
    fontSize: 9,
    fontWeight: '900',
    letterSpacing: 1,
  }
});

