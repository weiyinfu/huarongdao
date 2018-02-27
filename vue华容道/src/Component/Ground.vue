<!--背景组件
此组件包括一个矩形和一个多边形
-->
<template>
    <svg class="ground" :width="width" :height="height">
        <rect x="0" y="0" :width="width" :height="height"/>
        <polygon :points="points"/>
    </svg>
</template>

<script>

    export default {
        //将props暴露给父组件
        props: ['unitSize'],
        //计算属性
        computed: {
            width() {
                return this.unitSize * 5;
            },
            height() {
                return this.unitSize * 6.3;
            },
            points() {
                let unitSize = this.unitSize;
                return [
                    `${unitSize * 0.5},${unitSize * 0.8}`,
                    `${unitSize * 0.5},${unitSize * 5.8}`,
                    `${unitSize * 1.5},${unitSize * 5.8}`,
                    `${unitSize * 1.5},${unitSize * 6.3}`,
                    `${unitSize * 3.5},${unitSize * 6.3}`,
                    `${unitSize * 3.5},${unitSize * 5.8}`,
                    `${unitSize * 4.5},${unitSize * 5.8}`,
                    `${unitSize * 4.5},${unitSize * 0.8}`,
                    `${unitSize * 0.5},${unitSize * 0.8}`,
                ].join(' ');
            }
        }
    }

</script>

<style lang="less">

    .ground {
        rect {//长方形是灰色的
            fill: #888;
        }
        polygon {//多边形是白色的
            fill: #fff;
        }
    }

</style>