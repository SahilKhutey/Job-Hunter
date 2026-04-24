import React, { useEffect, useState } from 'react';
import { Text, StyleSheet, TextStyle } from 'react-native';

interface AnimatedNumberProps {
    value: number;
    style?: TextStyle;
}

export default function AnimatedNumber({ value, style }: AnimatedNumberProps) {
    const [display, setDisplay] = useState(0);

    useEffect(() => {
        let start = 0;
        if (value === 0) return;
        
        const duration = 1000; # 1 second
        const stepTime = 30;
        const totalSteps = duration / stepTime;
        const increment = value / totalSteps;

        const interval = setInterval(() => {
            start += increment;
            if (start >= value) {
                setDisplay(value);
                clearInterval(interval);
            } else {
                setDisplay(Math.floor(start));
            }
        }, stepTime);

        return () => clearInterval(interval);
    }, [value]);

    return <Text style={[styles.text, style]}>{display}</Text>;
}

const styles = StyleSheet.create({
    text: {
        color: '#fff',
        fontSize: 24,
        fontWeight: '700',
    }
});
