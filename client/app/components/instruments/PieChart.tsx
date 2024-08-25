"use client";

import React, { useEffect, useState } from 'react';
import dummydata from "../dummydata";
import useMetadataStore from '@/app/store/useMetadataStore';
import { ResponsivePie } from '@nivo/pie';

interface PieChartProps {
    symbol: string
}

const PieChart: React.FC<PieChartProps> = ({ symbol }) => {
    const instruments = useMetadataStore((state)=>state.instruments);
    

    const pieChartData = [
        {
            "id": "Training Loss",
            "label": "Training Loss",
            "value": instruments[symbol]?.results?.loss,
        },
        {
            "id": "Validation Loss",
            "label": "Validation Loss",
            "value": instruments[symbol]?.results?.val_loss,
        },
        {
            "id": "Accuracy",
            "label": "Accuracy",
            "value": instruments[symbol]?.results?.accuracy,  // Assuming you want to show accuracy as a percentage
        },
        {
            "id": "Validation Accuracy",
            "label": "Validation Accuracy",
            "value": instruments[symbol]?.results?.val_accuracy,  // Assuming you want to show validation accuracy as a percentage
        }
    ];

    return (
        <ResponsivePie
            data={pieChartData}
            margin={{ top: 5, right: 5, bottom: 5, left: 5 }}
            innerRadius={0.2}
            colors={{ scheme: 'greys' }}
            padAngle={3}
            activeOuterRadiusOffset={3}
            borderWidth={2}
            cornerRadius={2 }
            borderColor="#AAAE7F"
            arcLabel="value"
            enableArcLinkLabels={false}
            arcLinkLabelsSkipAngle={14}
            arcLinkLabelsTextColor="#333333"
            arcLinkLabelsThickness={5}
            arcLinkLabelsColor={{ from: 'color' }}
            arcLabelsTextColor={{
                from: 'color',
                modifiers: [
                    [
                        'darker',
                        3
                    ]
                ]
            }}
            defs={[
                {
                    id: 'train',
                    background: 'inherit',
                    type: 'patternLines',
                    padding: 1,
                    spacing: 3,
                    rotation: -45,
                    lineWidth: 0.5
                },
                {
                    id: 'valid',
                    background: 'inherit',
                    type: 'patternDots',
                    color: 'rgba(255, 255, 255, 0.3)',
                    size: 1,
                    padding: 0.4,
                    stagger: true
                },
            ]}
            fill={[
                {
                    match: {
                        id: 'Training Loss'
                    },
                    id: 'train'
                },
                {
                    match: {
                        id: 'Validation Loss'
                    },
                    id: 'valid'
                },
                {
                    match: {
                        id: 'Accuracy'
                    },
                    id: 'train'
                },
                {
                    match: {
                        id: 'Validation Accuracy'
                    },
                    id: 'valid'
                }
            ]}
            legends={[]}
        />
    );
};

export default PieChart;
