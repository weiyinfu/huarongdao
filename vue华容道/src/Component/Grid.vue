<template>
    <rect
            class="grid"
            :class="{ success }"
            :id="draging && 'draging'"
            :x="x"
            :y="y"
            :width="width"
            :height="height"
            :data-type="this.type"
            :stroke-width="this.unitSize / 25"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd"
            @mousedown="handleMouseDown"
            @mouseup="handleMouseUp"
    />
</template>

<script>

    export default {
        //这些属性是对外的接口
        props: ['type', 'position', 'startX', 'startY', 'unitSize', 'handleMove', 'success'],
        data() {
            return {
                draging: false,
                x: this.startX,
                y: this.startY,
                previousX: 0,
                previousY: 0
            }
        },
        watch: {
            startX(newValue) {
                this.x = newValue;
            },
            startY(newValue) {
                this.y = newValue;
            }
        },
        computed: {
            height() {
                switch (this.type) {
                    case '2':
                    case '4':
                        return this.unitSize;
                    case '3':
                    case '5':
                        return this.unitSize * 2;
                    default:
                        return 0;
                }
            },
            width() {
                switch (this.type) {
                    case '2':
                    case '3':
                        return this.unitSize;
                    case '4':
                    case '5':
                        return this.unitSize * 2;
                    default:
                        return 0;
                }
            }
        },
        methods: {
            handleTouchStart(e) {
                this.previousX = e.targetTouches[0].clientX;
                this.previousY = e.targetTouches[0].clientY;
                this.draging = true;
            },
            handleTouchMove(e) {
                let currentX = e.targetTouches[0].clientX;
                let currentY = e.targetTouches[0].clientY;
                //这就是vue的力量，直接更改数据就能改变样式
                this.x += currentX - this.previousX;
                this.y += currentY - this.previousY;
                this.previousX = currentX;
                this.previousY = currentY;
                let shiftX = this.x - this.startX;
                let shiftY = this.y - this.startY;
                let direction = 0;
                if (Math.abs(shiftY) > Math.abs(shiftX)) {
                    if (-shiftY > this.unitSize / 1.5) direction = 1;
                    else if (shiftY > this.unitSize / 1.5) direction = 3;
                } else {
                    if (shiftX > this.unitSize / 1.5) direction = 2;
                    else if (-shiftX > this.unitSize / 1.5) direction = 4;
                }
                this.handleMove(direction, this.position);
            },
            handleTouchEnd(e) {
                let _this = this, step = 5;
                let distanceX = _this.x - this.startX;
                let distanceY = _this.y - this.startY;
                let inv = setInterval(() => {
                    if (!--step) {
                        clearInterval(inv);
                        _this.draging = false;
                    }
                    _this.x = this.startX + distanceX * step * 0.1;
                    _this.y = this.startY + distanceY * step * 0.1;
                }, 10);
            },
            handleMouseDown(e) {
                let target = e.target;
                let event = document.createEvent('Events');
                event.initEvent('touchstart');
                event.targetTouches = [{clientX: e.clientX, clientY: e.clientY}];
                //mousemove跟touchmove是一样的，将mousemove事件封装成touchemove事件
                document.onmousemove = function (e) {
                    let event = document.createEvent('Events');
                    event.initEvent('touchmove');
                    event.targetTouches = [{clientX: e.clientX, clientY: e.clientY}];
                    target.dispatchEvent(event);
                }
                target.dispatchEvent(event);
            },
            handleMouseUp(e) {
                //移除掉mousemove事件处理器
                document.onmousemove = null;
                let event = document.createEvent('Events');
                event.initEvent('touchend');
                e.target.dispatchEvent(event);
            }
        }
    }

</script>

<style lang="less">
    .grid {
        fill: #09c;
        stroke: #fff;

        &#draging {
            stroke: #0ff;
        }

        &[data-type="5"] {
            fill: #f44;

            &.success {
                fill: #0a0;
            }
        }
    }
</style>