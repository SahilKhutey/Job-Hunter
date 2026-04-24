import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { api } from '../services/api';

export default function AnalyticsScreen() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/analytics/dashboard')
            .then(res => setStats(res.data.stats))
            .catch(err => console.log(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <ActivityIndicator size="large" color="#fff" style={{flex: 1, backgroundColor: '#0a0a0a'}} />;

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Intelligence</Text>
            
            <View style={styles.statsGrid}>
                <View style={styles.statBox}>
                    <Text style={styles.statVal}>{stats?.total_applications || 0}</Text>
                    <Text style={styles.statLabel}>Total Apps</Text>
                </View>
                <View style={styles.statBox}>
                    <Text style={[styles.statVal, {color: '#3b82f6'}]}>{stats?.interview_rate || 0}%</Text>
                    <Text style={styles.statLabel}>Interview Rate</Text>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0a0a0a',
        padding: 20,
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 20,
    },
    statsGrid: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    statBox: {
        backgroundColor: '#171717',
        width: '48%',
        padding: 20,
        borderRadius: 16,
        alignItems: 'center',
    },
    statVal: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    },
    statLabel: {
        color: '#a3a3a3',
        marginTop: 4,
    }
});
