<template>
    <div class="indexBox" :style="{height:winHeight}">
        <img class="indexTitles" src="/static/image/indexTitle.png" alt="">
        <img class="indexBanners" src="/static/image/indexBanner.png" alt="">
        <a class="indexBottom" @click.stop="home">
            <img src="/static/image/indexBtn.png" alt="">
        </a>
    </div>
</template>

<script type="text/ecmascript-6">
    import router from '../router/index'

    export default {
        data() {
            return {
                winHeight: $(window).innerHeight() + 'px'
            };
        },
        components: {},
        methods: {
            home: function () {
                router.push({path: '/home'})
            }
        }
    };
</script>

<style>
</style>
