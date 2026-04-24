import React from 'react';
import { View, Text, StyleSheet, ScrollView, SafeAreaView } from 'react-native';
import Card from '../../components/Card';
import AnimatedNumber from '../../components/AnimatedNumber';
import { useSocket } from '../../hooks/useSocket';

export default function Dashboard() {
    useSocket();

    return (
        <SafeAreaView style={styles.safe}>
            <ScrollView contentContainerStyle={styles.container}>
                <View style={styles.header}>
                    <Text style={styles.greeting}>Mission Control</Text>
                    <Text style={styles.subGreeting}>System Status: Operational</Text>
                </View>

                <View style={styles.statsRow}>
                    <Card style={styles.statCard}>
                        <Text style={styles.statLabel}>Applications</Text>
                        <AnimatedNumber value={124} style={styles.statVal} />
                    </Card>
                    <Card style={styles.statCard}>
                        <Text style={styles.statLabel}>Interviews</Text>
                        <AnimatedNumber value={12} style={[styles.statVal, {color: '#6366F1'}]} />
                    </Card>
                </View>

                <Text style={styles.sectionTitle}>Agent Activity</Text>
                <Card style={styles.activityCard}>
                    <Text style={styles.activityLog}>[ExecutionAgent] Navigating to target...</Text>
                    <View style={styles.divider} />
                    <Text style={styles.activityLog}>[VisionAgent] Analyzing DOM structure...</Text>
                </Card>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safe: {
        flex: 1,
        backgroundColor: '#000',
    },
    container: {
        padding: 20,
    },
    header: {
        marginBottom: 32,
        marginTop: 10,
    },
    greeting: {
        fontSize: 32,
        fontWeight: '800',
        color: '#fff',
        letterSpacing: -0.5,
    },
    subGreeting: {
        color: '#71717A',
        fontSize: 16,
        marginTop: 4,
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 32,
    },
    statCard: {
        width: '48%',
    },
    statLabel: {
        color: '#A1A1AA',
        fontSize: 13,
        fontWeight: '500',
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginBottom: 8,
    },
    statVal: {
        fontSize: 32,
    },
    sectionTitle: {
        color: '#fff',
        fontSize: 20,
        fontWeight: '700',
        marginBottom: 16,
    },
    activityCard: {
        width: '100%',
    },
    activityLog: {
        color: '#D4D4D8',
        fontSize: 14,
        fontFamily: 'System', # Platform specific logic would be better here
        marginVertical: 4,
    },
    divider: {
        height: 1,
        backgroundColor: 'rgba(255,255,255,0.05)',
        marginVertical: 12,
    }
});
