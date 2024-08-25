"use client";

import React, { useEffect, useState } from 'react';
import { ResponsiveBar } from '@nivo/bar';
import dummydata from "../dummydata"
import useMetadataStore from '@/app/store/useMetadataStore';

interface TrainingBarDatum {
    timestamp: string;
    training_loss: number;
    validation_loss: number;
    accuracy: number;
    learning_rate: number;
}

interface BarChartProps {
    symbol: string
}

const BarChart: React.FC<BarChartProps> = ({ symbol }) => {
    const [chartData, setChartData] = useState<TrainingBarDatum[]>([]);
    const instruments = useMetadataStore((state)=>state.instruments)
    useEffect(() => {
        console.log(instruments[symbol].models)
       
    }, []);

    return (
        <ResponsiveBar
            data={dummydata}
            keys={['training_loss', 'validation_loss', 'accuracy', 'learning_rate']}
            indexBy="timestamp"
            margin={{ top: 0, right: 0, bottom: 0, left: 60 }}
            padding={0}
            layout="horizontal"
            valueScale={{ type: 'linear' }}
            indexScale={{ type: 'band', round: true }}
            colors={{ scheme: 'purple_blue_green' }}           
            borderColor={{
                from: 'color',
                modifiers: [['darker', 1.6]],
            }}
            axisTop={null}
            axisRight={null}
            axisBottom={null}
            axisLeft={{
                tickSize: 5,
                tickPadding: 5,
                tickRotation: 0,
                legendPosition: 'middle',
                legendOffset: -40,
            }}
            enableGridX={false}
            enableGridY={false}
            labelSkipWidth={12}
            labelSkipHeight={12}
            labelTextColor={{
                from: 'color',
                modifiers: [['darker', 2.4]],
            }}
            legends={[]}
            role="application"
            ariaLabel="Training result data"
            barAriaLabel={(e) => `${e.id}: ${e.formattedValue} at ${e.indexValue}`}
        />
    );
};

export default BarChart
