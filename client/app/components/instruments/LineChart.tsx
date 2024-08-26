// LineChart.tsx
import React from 'react';
import { ResponsiveLine } from '@nivo/line';
import {chartData} from "../dummydata"

interface LineChartProps {
    symbol: string;
}

export type SymbolType = string;

export interface DataPoint {
    x: number; // Epoch or time point
    y: number; // Loss value
}

export interface ChartData {
    id: string; // Identifier for the dataset (e.g., 'Training Loss' or 'Validation Loss')
    color: string; // Color for the line in the chart
    data: DataPoint[]; // Array of data points
}

const LineChart: React.FC<LineChartProps> = ({ symbol }) => (
    <ResponsiveLine
        data={chartData}
        margin={{ top: 10, right: 10, bottom: 30, left: 30 }}
        xScale={{ type: 'point' }}
        yScale={{
            type: 'linear',
            min: 'auto',
            max: 'auto',
            stacked: true,
            reverse: false
        }}
        lineWidth={2}
        axisTop={null}
        axisRight={null}
        axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legendOffset: 36,
            legendPosition: 'middle',
            truncateTickAt: 0
        }}
        axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legendOffset: -40,
            legendPosition: 'middle',
            truncateTickAt: 0
        }}
        enableGridX={false}
        pointSize={5}
        pointColor={{ from: 'color', modifiers: [] }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabel="data.yFormatted"
        pointLabelYOffset={-11}
        areaOpacity={0.45}
        enableCrosshair={false}
        useMesh={true}
        legends={[
            {
                anchor: 'top-right',
                direction: 'column',
                justify: false,
                translateX: -1,
                translateY: 1,
                itemsSpacing: 0,
                itemDirection: 'left-to-right',
                itemWidth: 94,
                itemHeight: 20,
                itemOpacity: 0.75,
                symbolSize: 12,
                symbolShape: 'circle',
                symbolBorderColor: 'rgba(0, 0, 0, .5)',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemBackground: 'rgba(0, 0, 0, .03)',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
);

export default LineChart;