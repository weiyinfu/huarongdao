<template>
    <div id="main">
        <!--main中包含四个部分：-->
        <!--Ground：背景-->
        <!--Board：棋盘-->
        <!--按钮：选择关卡按钮-->
        <!--Level：选关-->
        <!--这四部分之间都不是包含关系，而是并列关系-->
        <!--自己定义的组件Ground有prop（插槽）接受属性-->
        <Ground :unitSize="unitSize"
                style="position: absolute; top: 0; left: 0;"/>
        <Board :unitSize="unitSize"
               :layout="layout"
               :style="{ position: 'absolute', top: unitSize * 0.8, left: unitSize * 0.5 }"/>
        <div :style="{ top: `${(unitSize * 0.8 - 34) / 2}px`, left: `${(unitSize * 5 - 124) / 2}px` }"
             class="select-btn"
             @click="showLevel = true;">{{ title }}
        </div>
        <Level :unitSize="unitSize"
               :show="showLevel"
               :handleSelect="handleSelect"/>
    </div>
</template>

<script>

    import Ground from './Component/Ground.vue';
    import Board from './Component/Board.vue';
    import Level from './Component/Level.vue';

    export default {
        components: {Ground, Board, Level},
        data() {
            return {
                //每个小方块的大小
                unitSize: window.innerWidth / 5,
                //初始布局
                layout: '22222222222222222222',
                title: '选择关卡',
                showLevel: false
            }
        },
        methods: {
            /**
             * 选择level之后
             * */
            handleSelect(level) {
                this.layout = level.layout;
                this.title = level.title;
                this.showLevel = false;
            }
        },
        /**
         * 拦截Vue的生命周期
         * */
        created() {
            //如果location.hash值不为空，那么更改layout和title两个变量
            location.hash && (this.layout = location.hash.slice(1)) && (this.title = '自定义');
            //适应屏幕尺寸变化，这里大量使用lambda表达式，从而可以
            // 继续使用this来访问data中的变量
            window.onresize = () => this.unitSize = window.innerWidth / 5;
            //监听窗口hash变化，hash值表示局面
            window.onhashchange = () => location.hash &&
                (this.layout = location.hash.slice(1)) && (this.title = '自定义');

        }
    }

</script>

<style lang="less">

    #main {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;

        .select-btn {
            position: absolute;
            background-color: #ccc;
            border: 2px solid #aaa;
            border-radius: 5px;
            min-width: 120px;
            line-height: 30px;
            text-align: center;
            cursor: pointer;

            &:hover {
                background-color: #eee;
            }

            &:active {
                color: #09c;
            }
        }
    }

</style>
