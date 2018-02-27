<template>
    <!--禁用掉棋盘自身的touchstart-->
    <svg :width="width" :height="height"
         @touchstart="e => e.preventDefault()">
        <!--棋子列表-->
        <Grid
                v-for="(t, i) in state"
                v-if="t !== '1' && t != '0'"
                :type="t"
                :position="i"
                :key="`grid-${i}`"
                :success="t === '5' && success"
                :unitSize="unitSize"
                :startX="(i % 4) * unitSize"
                :startY="Math.floor(i / 4) * unitSize"
                :handleMove="handleMove"
        />
        <rect class="tip" :class="{ success, thinking }"
              :x="unitSize * 1.2" :y="unitSize * 5.05"
              :width="unitSize * 1.6" :height="unitSize * 0.4"
              @click="help" @touchstart="help"/>
        <use xlink:href="#draging"/>
    </svg>
</template>

<script>

    import Grid from './Grid.vue';
    import core from '../core.js'

    export default {
        components: {Grid},
        props: ['unitSize', 'layout'],
        data() {
            return {
                state: this.layout,
                answer: [],
                thinking: false
            };
        },
        computed: {
            width() {
                return this.unitSize * 4;
            },
            height() {
                return this.unitSize * 5.5;
            },
            success() {
                return this.state[13] === '5';
            }
        },
        watch: {
            layout(newValue) {
                this.state = newValue;
                this.answer = [];
            }
        },
        methods: {
            handleMove(direction, position) {
                let nextState = false;
                switch (direction) {
                    case 1:
                        nextState = core.moveUp(this.state, position);
                        break;
                    case 2:
                        nextState = core.moveRight(this.state, position);
                        break;
                    case 3:
                        nextState = core.moveDown(this.state, position);
                        break;
                    case 4:
                        nextState = core.moveLeft(this.state, position);
                        break;
                }
                nextState && (this.state = nextState) && (this.answer = []);
            },
            help() {
                this.thinking = true;
                //10ms之后判断answer中的内容，如果answer中已经有答案直接利用
                //如果answer中没有答案，则调用core.getSolve()进行求解
                setTimeout(() => {
                    if (!this.answer.length)
                        this.answer = core.getSolve(this.state);
                    if (this.answer.length)
                        this.state = this.answer.pop();
                    this.thinking = false;
                }, 10);
            }
        }
    }

</script>
<!--使用less，编译成css-->
<style lang="less">

    svg {
        //居中显示
        margin: 0 auto;

        .tip {
            fill: #0a0;
            //正在思考时，按钮的填充色
            &.thinking {
                fill: #f44;
            }
            //找到答案后，按钮的填充色
            &.success {
                fill: #fff;
            }
        }
    }

</style>