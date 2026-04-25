import React, { useEffect, useState } from 'react';
import { 
    View, Text, StyleSheet, ActivityIndicator, 
    ScrollView, Dimensions, Platform 
} from 'react-native';
import { api } from '../services/api';
import { 
    TrendingUp, BarChart3, Sparkles, 
    Target, Zap, ArrowUpRight 
} from 'lucide-react-native';

const { width } = Dimensions.get('window');

export default function AnalyticsScreen() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/analytics/dashboard')
            .then(res => setStats(res.data.stats || res.data))
            .catch(err => console.log(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#7c3aed" />
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Career Intelligence</Text>
                <View style={styles.badge}>
                    <TrendingUp color="#10b981" size={12} />
                    <Text style={styles.badgeText}>+12% vs last week</Text>
                </View>
            </View>

            <ScrollView contentContainerStyle={styles.scrollContent}>
                <View style={styles.insightCard}>
                    <View style={styles.insightHeader}>
                        <Sparkles color="#7c3aed" size={16} />
                        <Text style={styles.insightTitle}>Strategic Insight</Text>
                    </View>
                    <Text style={styles.insightText}>
                        Your "Full Stack Senior" resume is currently outperforming others with a 24% higher interview conversion rate.
                    </Text>
                    <View style={styles.insightFooter}>
                        <Text style={styles.insightRecommendation}>RECOMMENDATION: Prioritize LinkedIn applications for high-match roles.</Text>
                    </View>
                </View>

                <View style={styles.statsGrid}>
                    <View style={styles.statCard}>
                        <View style={[styles.iconBox, { backgroundColor: '#7c3aed15' }]}>
                            <Target color="#7c3aed" size={18} />
                        </View>
                        <Text style={styles.statVal}>{stats?.total_applications || 0}</Text>
                        <Text style={styles.statLabel}>Total Apps</Text>
                    </View>

                    <View style={styles.statCard}>
                        <View style={[styles.iconBox, { backgroundColor: '#10b98115' }]}>
                            <BarChart3 color="#10b981" size={18} />
                        </View>
                        <Text style={styles.statVal}>{stats?.interview_rate || 0}%</Text>
                        <Text style={styles.statLabel}>Interview Rate</Text>
                    </View>
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Conversion Funnel</Text>
                    <View style={styles.funnelCard}>
                        <View style={styles.funnelRow}>
                            <Text style={styles.funnelLabel}>Applications</Text>
                            <Text style={styles.funnelValue}>{stats?.total_applications || 0}</Text>
                        </View>
                        <View style={styles.funnelBarContainer}>
                            <View style={[styles.funnelBar, { width: '100%', backgroundColor: '#7c3aed' }]} />
                        </View>
                        
                        <View style={[styles.funnelRow, { marginTop: 16 }]}>
                            <Text style={styles.funnelLabel}>Interviews</Text>
                            <Text style={styles.funnelValue}>{stats?.interviews || 0}</Text>
                        </View>
                        <View style={styles.funnelBarContainer}>
                            <View style={[styles.funnelBar, { width: `${stats?.interview_rate || 20}%`, backgroundColor: '#3b82f6' }]} />
                        </View>
                    </View>
                </View>

                <View style={{ height: 100 }} />
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0a0a0a',
    },
    loadingContainer: {
        flex: 1,
        backgroundColor: '#0a0a0a',
        alignItems: 'center',
        justifyContent: 'center',
    },
    header: {
        paddingHorizontal: 24,
        paddingTop: Platform.OS === 'ios' ? 60 : 40,
        paddingBottom: 20,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: 22,
        fontWeight: 'bold',
        color: '#fff',
    },
    badge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#10b98110',
        paddingHorizontal: 10,
        paddingVertical: 6,
        borderRadius: 12,
        gap: 6,
    },
    badgeText: {
        color: '#10b981',
        fontSize: 10,
        fontWeight: 'bold',
    },
    scrollContent: {
        padding: 24,
    },
    insightCard: {
        backgroundColor: '#7c3aed08',
        borderRadius: 24,
        padding: 20,
        borderWidth: 1,
        borderColor: '#7c3aed20',
        marginBottom: 24,
    },
    insightHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        marginBottom: 12,
    },
    insightTitle: {
        color: '#a78bfa',
        fontSize: 14,
        fontWeight: 'bold',
    },
    insightText: {
        color: '#d4d4d4',
        fontSize: 13,
        lineHeight: 20,
        marginBottom: 16,
    },
    insightFooter: {
        borderTopWidth: 1,
        borderTopColor: '#7c3aed15',
        paddingTop: 12,
    },
    insightRecommendation: {
        color: '#7c3aed',
        fontSize: 10,
        fontWeight: 'bold',
        textTransform: 'uppercase',
    },
    statsGrid: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 32,
    },
    statCard: {
        backgroundColor: '#171717',
        width: (width - 64) / 2,
        padding: 20,
        borderRadius: 24,
        borderWidth: 1,
        borderColor: '#262626',
    },
    iconBox: {
        width: 36,
        height: 36,
        borderRadius: 12,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 12,
    },
    statVal: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    },
    statLabel: {
        color: '#525252',
        fontSize: 12,
        marginTop: 4,
        fontWeight: '500',
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
        marginBottom: 16,
    },
    funnelCard: {
        backgroundColor: '#171717',
        padding: 24,
        borderRadius: 24,
        borderWidth: 1,
        borderColor: '#262626',
    },
    funnelRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        marginBottom: 8,
    },
    funnelLabel: {
        color: '#a3a3a3',
        fontSize: 13,
        fontWeight: '500',
    },
    funnelValue: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
    funnelBarContainer: {
        height: 6,
        backgroundColor: '#0a0a0a',
        borderRadius: 3,
        width: '100%',
        overflow: 'hidden',
    },
    funnelBar: {
        height: '100%',
        borderRadius: 3,
    }
});
