<template>
    <div class="hello" :style="{height:winHeight}">
        <div v-if="ok">
            <div class="jtBox" :style="{height:winHeight}">
                <div class="headerTitle">
                    <img class="ckt" :src="list.cks" alt="">
                    <div class="bushuBg">
                        <img src="/static/image/bushu.png" alt="">
                        <span>{{num}}</span>
                    </div>
                </div>
                <ul class="ptBox" :style="{height:ulHeight}">
                    <img :src="list.cks" alt="" class="ptCkt">
                </ul>
                <img class="tishis" src="/static/image/erms.png" alt="">
                <!-- <div class="eqm">
                  <img src="/static/image/erm.png" alt="">
                </div> -->
            </div>
            <span class="cabc">长按图片保存</span>
        </div>
        <div v-else>
            <div class="shareBox" :style="{height:winHeight}" v-show="fxShow">
                <img class="fximg" src="/static/image/fenxiang.png" alt="">
                <a class="closeBtn" @click.stop="close">
                    <img src="/static/image/gbBtn.png" alt="">
                </a>
            </div>
            <div class="headerTitle">
                <img class="ckt" :src="list.cks" alt="">
                <div class="bushuBg">
                    <img src="/static/image/bushu.png" alt="">
                    <span>{{num}}</span>
                </div>
            </div>
            <a class="hyzBtn" @click.stop="hyzBtn">
                <img src="/static/image/hyz.png" alt="">
            </a>
            <ul class="ptBox">
                <img v-show="cktShow" :src="list.cks" alt="" class="ptCkt">
                <li @click="iclick(index)" v-for="(item,index) in list.listing" :val="item.name"
                    :style="{backgroundImage: 'url('+item.img+')',height:liHeights}">
                    <!-- <img :src="item.img" alt=""> -->
                </li>
            </ul>
            <img class="tishi" src="/static/image/tishi.png" alt="">
            <a class="homeBtn" @click.stop="goto" v-if="shows">
                <img src="/static/image/kaishi.png" alt="">
            </a>
            <div class="indexBtns" v-else>
                <a @click.stop="start">
                    <img src="/static/image/congxinkaishi.png" alt="">
                </a>
                <a @click.stop="share">
                    <img src="/static/image/yuezhanhaoyou.png" alt="">
                </a>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from "vue";
    import html2canvas from "../../static/js/html2canvas.min.js";

    export default {
        name: "HelloWorld",
        data() {
            return {
                msg: "Welcome to Your Vue.js App",
                cktShow: true,
                fxShow: false,
                ok: false,
                winHeight: $(window).innerHeight() + "px",
                jtHeight: $(window).innerHeight() + 20 + "px",
                liHeights: ($(window).innerWidth() - 40) / 3 + "px",
                ulHeight: $(window).innerWidth() - 20 + 'px',
                list: {
                    cks: "/static/image/1/ckt.jpg",
                    listing: [{
                        name: "1",
                        img: "/static/image/1/1.jpg"
                    },
                        {
                            name: "2",
                            img: "/static/image/1/2.jpg"
                        },
                        {
                            name: "3",
                            img: "/static/image/1/3.jpg"
                        },
                        {
                            name: "4",
                            img: "/static/image/1/4.jpg"
                        },
                        {
                            name: "5",
                            img: "/static/image/1/5.jpg"
                        },
                        {
                            name: "6",
                            img: "/static/image/1/6.jpg"
                        },
                        {
                            name: "7",
                            img: "/static/image/1/7.jpg"
                        },
                        {
                            name: "8",
                            img: "/static/image/1/8.jpg"
                        }
                    ]
                },
                liHeight: "",
                num: 0,
                shows: true,
                kbimg: '/static/image/tbg.jpg',
                newA: ''
            };
        },

        created() {
            let that = this;
            let kk = that.list;
            kk.listing.push("");
            that.liHeight =
                $("li")
                    .width() + "px";
            // setTimeout(function() {
            //   $('li').height((that.winHeight -40)/3)
            //   // $("li").css({
            //   //   height: (that.winHeight -40)/3 +'px'
            //   // });
            // }, 800);
        },
        methods: {
            iclick: function (index) {
                let that = this;

                let curNum = that.list.listing[index],
                    leftNum = that.list.listing[index - 1],
                    rightNum = that.list.listing[index + 1],
                    topNum = that.list.listing[index - 3],
                    bottomNum = that.list.listing[index + 3];
                if (rightNum === "" && 2 !== index % 3) {
                    Vue.set(that.list.listing, index + 1, curNum);
                    Vue.set(that.list.listing, index, '');
                } else if (topNum === "") {
                    Vue.set(that.list.listing, index - 3, curNum);
                    Vue.set(that.list.listing, index, '');
                } else if (bottomNum === "") {
                    Vue.set(that.list.listing, index + 3, curNum);
                    Vue.set(that.list.listing, index, '');
                } else if (leftNum === "" && index % 3) {
                    Vue.set(that.list.listing, index - 1, curNum);
                    Vue.set(that.list.listing, index, '');
                }
                that.passFn();
                // console.log(that.list.listing)
                that.num++;
                // console.log(that.num++)
            },
            goto: function () {
                let that = this;
                that.list.listing.sort(function () {
                    return Math.random() > 0.5;
                });
                that.shows = false;
                that.cktShow = false;
            },
            start: function () {
                let that = this;
                that.list.listing.sort(function () {
                    return Math.random() > 0.5;
                });
                that.num = 0;
                // that.cktShow= true;
            },
            share: function () {
                let that = this;
                that.fxShow = true;
            },
            close: function () {
                let that = this;
                that.fxShow = false;
            },
            passFn() {
                let that = this;

                if (that.list.listing[8] === '') {
                    var html;
                    let newPuzzles = this.list.listing.slice(0, 7)
                    for (let i = 0; i < 7; i++) {
                        html += newPuzzles[i].name
                    }
                    console.log(html)

                    if (html === 'undefined1234567') {
                        // setTimeout(function() {
                        //   alert("ok")
                        // },100)
                        let cb = that.num - 27
                        if (that.num > 0 && that.num < 30) {
                            $('title').text('我的天啊！传说中的大神！' + that.num + '步完成！来挑战吧！')
                        }
                        if (that.num > 31 && that.num < 50) {
                            $('title').html('厉害！' + that.num + '步完成！离大神差' + cb + '步！来挑战吧！')
                        }
                        if (that.num > 51 && that.num < 90) {
                            $('title').html(+that.num + '步完成！成绩不错！再接再厉!来挑战吧！')
                        }
                        if (that.num > 91 && that.num < 110) {
                            $('title').html(+that.num + '步完成！小学二年级水平！来挑战吧！')
                        }
                        if (that.num > 111 && that.num < 130) {
                            $('title').html(+that.num + '步完成！小学一年级水平！来挑战吧！')
                        }
                        if (that.num > 131 && that.num < 170) {
                            $('title').html(+that.num + '步完成！幼儿园水平也不过这样了！来挑战吧！')
                        }
                        if (that.num > 171) {
                            $('title').html(+that.num + '步完成！亲人我觉得你需要重生了！来挑战吧！')
                        }
                        that.ok = true
                        setTimeout(function () {
                            html2canvas($('.jtBox'), {
                                onrendered: function (canvas) {
                                    var image = canvas.toDataURL("image/png");
                                    var pHtml =
                                        "<img class='endImg' style='border-radius:0px;border:0px;' src=" +
                                        image +
                                        " />";
                                    // $("#html2canvas").html(pHtml);
                                    $('body').append(pHtml)
                                }
                            });
                        }, 200);
                    }


                }
            },
            hyzBtn: function () {

                let that = this;
                that.num = 0;
                that.cktShow = true;
                that.shows = true;
                let listImg = [{
                    cks: "/static/image/2/ckt.jpg",
                    listing: [{
                        name: "1",
                        img: "/static/image/2/1.jpg"
                    },
                        {
                            name: "2",
                            img: "/static/image/2/2.jpg"
                        },
                        {
                            name: "3",
                            img: "/static/image/2/3.jpg"
                        },
                        {
                            name: "4",
                            img: "/static/image/2/4.jpg"
                        },
                        {
                            name: "5",
                            img: "/static/image/2/5.jpg"
                        },
                        {
                            name: "6",
                            img: "/static/image/2/6.jpg"
                        },
                        {
                            name: "7",
                            img: "/static/image/2/7.jpg"
                        },
                        {
                            name: "8",
                            img: "/static/image/2/8.jpg"
                        }
                    ]
                },
                    {
                        cks: "/static/image/1/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/1/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/1/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/1/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/1/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/1/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/1/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/1/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/1/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/3/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/3/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/3/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/3/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/3/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/3/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/3/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/3/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/3/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/4/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/4/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/4/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/4/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/4/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/4/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/4/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/4/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/4/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/5/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/5/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/5/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/5/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/5/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/5/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/5/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/5/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/5/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/6/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/6/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/6/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/6/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/6/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/6/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/6/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/6/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/6/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/7/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/7/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/7/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/7/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/7/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/7/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/7/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/7/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/7/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/8/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/8/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/8/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/8/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/8/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/8/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/8/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/8/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/8/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/9/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/9/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/9/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/9/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/9/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/9/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/9/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/9/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/9/8.jpg"
                            }
                        ]
                    },
                    {
                        cks: "/static/image/10/ckt.jpg",
                        listing: [{
                            name: "1",
                            img: "/static/image/10/1.jpg"
                        },
                            {
                                name: "2",
                                img: "/static/image/10/2.jpg"
                            },
                            {
                                name: "3",
                                img: "/static/image/10/3.jpg"
                            },
                            {
                                name: "4",
                                img: "/static/image/10/4.jpg"
                            },
                            {
                                name: "5",
                                img: "/static/image/10/5.jpg"
                            },
                            {
                                name: "6",
                                img: "/static/image/10/6.jpg"
                            },
                            {
                                name: "7",
                                img: "/static/image/10/7.jpg"
                            },
                            {
                                name: "8",
                                img: "/static/image/10/8.jpg"
                            }
                        ]
                    }
                ];
                let sss = Math.floor(Math.random() * 10);
                that.list = listImg[sss];
                console.log(listImg[sss]);
                let kk = that.list;
                kk.listing.push("");

            }
        }
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
