import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useSocket } from '../hooks/useSocket';

export default function DashboardScreen() {
    useSocket(); # Start live monitoring

    return (
        <View style={styles.container}>
            <ScrollView contentContainerStyle={styles.scroll}>
                <Text style={styles.title}>Mission Control</Text>
                
                <View style={styles.statusCard}>
                    <Text style={styles.statusLabel}>Agent Status</Text>
                    <Text style={styles.statusValue}>Monitoring Active 🛰️</Text>
                </View>

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Live Feed</Text>
                    <View style={styles.logItem}>
                        <Text style={styles.logText}>[ExecutionAgent] Ready for next mission...</Text>
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
        padding: 20,
    },
    scroll: {
        paddingBottom: 40,
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#fff',
        marginBottom: 20,
    },
    statusCard: {
        backgroundColor: '#171717',
        padding: 20,
        borderRadius: 16,
        borderWidth: 1,
        borderColor: '#262626',
        marginBottom: 24,
    },
    statusLabel: {
        color: '#a3a3a3',
        fontSize: 14,
        marginBottom: 4,
    },
    statusValue: {
        color: '#10b981',
        fontSize: 18,
        fontWeight: '600',
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#fff',
        marginBottom: 12,
    },
    logItem: {
        backgroundColor: '#171717',
        padding: 12,
        borderRadius: 8,
        marginBottom: 8,
    },
    logText: {
        color: '#d4d4d4',
        fontFamily: 'Courier',
        fontSize: 13,
    }
});
