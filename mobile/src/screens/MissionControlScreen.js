import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, FlatList, TouchableOpacity, ScrollView } from 'react-native';
import { Shield, Zap, Activity, ChevronRight, Terminal, Globe } from 'lucide-react-native';

function MissionLogItem({ log }) {
    return (
        <View style={styles.logItem}>
            <View style={styles.logTimeContainer}>
                <Text style={styles.logTime}>{log.time}</Text>
                <View style={styles.logConnector} />
            </View>
            <View style={styles.logContent}>
                <Text style={styles.logMessage}>{log.message}</Text>
                <Text style={styles.logAgent}>{log.agent}</Text>
            </View>
        </View>
    );
}

export default function MissionControlScreen() {
    const [missions, setMissions] = useState([
        {
            id: '1',
            job: 'Senior Full Stack Engineer',
            company: 'Stripe',
            status: 'Running',
            progress: 0.65,
            logs: [
                { id: 'l1', time: '12:45', agent: 'VisionAgent', message: 'Analyzing form structure...' },
                { id: 'l2', time: '12:46', agent: 'AutomationAgent', message: 'Filling contact information...' },
                { id: 'l3', time: '12:47', agent: 'AutomationAgent', message: 'Uploading tailored resume...' },
            ]
        }
    ]);

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Mission Control</Text>
                <View style={styles.activeBadge}>
                    <Activity color="#10b981" size={14} />
                    <Text style={styles.activeText}>1 ACTIVE</Text>
                </View>
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                {missions.map(mission => (
                    <View key={mission.id} style={styles.missionCard}>
                        <View style={styles.missionHeader}>
                            <View style={styles.missionInfo}>
                                <Text style={styles.missionJob}>{mission.job}</Text>
                                <Text style={styles.missionCompany}>{mission.company}</Text>
                            </View>
                            <View style={styles.statusBadge}>
                                <Text style={styles.statusText}>{mission.status}</Text>
                            </View>
                        </View>

                        <View style={styles.progressContainer}>
                            <View style={styles.progressTrack}>
                                <View style={[styles.progressFill, { width: `${mission.progress * 100}%` }]} />
                            </View>
                            <Text style={styles.progressText}>{Math.round(mission.progress * 100)}% Complete</Text>
                        </View>

                        <View style={styles.logSection}>
                            <View style={styles.logHeader}>
                                <Terminal color="#a3a3a3" size={14} />
                                <Text style={styles.logTitle}>Live Intelligence Stream</Text>
                            </View>
                            <View style={styles.logList}>
                                {mission.logs.map(log => (
                                    <MissionLogItem key={log.id} log={log} />
                                ))}
                            </View>
                        </View>

                        <TouchableOpacity style={styles.abortButton}>
                            <Text style={styles.abortText}>Abort Mission</Text>
                        </TouchableOpacity>
                    </View>
                ))}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0a0a0a',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingTop: 60,
        paddingBottom: 20,
    },
    title: {
        color: '#fff',
        fontSize: 24,
        fontWeight: 'bold',
    },
    activeBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#10b98115',
        paddingHorizontal: 10,
        paddingVertical: 5,
        borderRadius: 8,
        gap: 6,
        borderWidth: 1,
        borderColor: '#10b98133',
    },
    activeText: {
        color: '#10b981',
        fontSize: 10,
        fontWeight: 'bold',
    },
    content: {
        padding: 20,
    },
    missionCard: {
        backgroundColor: '#171717',
        borderRadius: 24,
        padding: 20,
        borderWidth: 1,
        borderColor: '#262626',
        marginBottom: 20,
    },
    missionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: 20,
    },
    missionJob: {
        color: '#fff',
        fontSize: 18,
        fontWeight: 'bold',
    },
    missionCompany: {
        color: '#737373',
        fontSize: 14,
        marginTop: 2,
    },
    statusBadge: {
        backgroundColor: '#7c3aed15',
        paddingHorizontal: 10,
        paddingVertical: 4,
        borderRadius: 6,
        borderWidth: 1,
        borderColor: '#7c3aed33',
    },
    statusText: {
        color: '#a78bfa',
        fontSize: 10,
        fontWeight: 'bold',
    },
    progressContainer: {
        marginBottom: 24,
    },
    progressTrack: {
        height: 6,
        backgroundColor: '#0a0a0a',
        borderRadius: 3,
        overflow: 'hidden',
        marginBottom: 8,
    },
    progressFill: {
        height: '100%',
        backgroundColor: '#7c3aed',
    },
    progressText: {
        color: '#525252',
        fontSize: 11,
        fontWeight: '500',
    },
    logSection: {
        backgroundColor: '#0a0a0a',
        borderRadius: 16,
        padding: 16,
        marginBottom: 20,
    },
    logHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        marginBottom: 16,
    },
    logTitle: {
        color: '#525252',
        fontSize: 11,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    logList: {
        paddingLeft: 4,
    },
    logItem: {
        flexDirection: 'row',
        marginBottom: 12,
    },
    logTimeContainer: {
        width: 45,
        alignItems: 'center',
    },
    logTime: {
        color: '#404040',
        fontSize: 10,
        fontWeight: '600',
    },
    logConnector: {
        width: 1,
        flex: 1,
        backgroundColor: '#171717',
        marginVertical: 4,
    },
    logContent: {
        flex: 1,
        paddingLeft: 12,
    },
    logMessage: {
        color: '#d4d4d4',
        fontSize: 13,
        lineHeight: 18,
    },
    logAgent: {
        color: '#7c3aed',
        fontSize: 10,
        fontWeight: 'bold',
        marginTop: 2,
    },
    abortButton: {
        height: 50,
        borderRadius: 14,
        borderWidth: 1,
        borderColor: '#ef444433',
        alignItems: 'center',
        justifyContent: 'center',
    },
    abortText: {
        color: '#ef4444',
        fontSize: 14,
        fontWeight: 'bold',
    }
});
