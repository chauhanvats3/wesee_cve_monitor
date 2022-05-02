<template>
  <div class="login-box">
    <input type="text" class="txtbox" id="user" placeholder="username" />

    <input type="password" class="txtbox" id="pass" placeholder="password" />

    <button class="button">Login</button>
  </div>
</template>

<script>
export default {}
</script>

<style lang="sass" scoped>
.login-box
    @include flexify-col
    margin: 20px
    padding: 20px
    background: rgba(216, 216, 216, 0.5)
    backdrop-filter: blur(10px)
    border-radius: 15px

    .txtbox
        margin: 10px 0px
        border: none
        border-radius: 10px
        font-size: 1.2rem
        padding: 15px
        width: 100%

    .button
        border-radius: 5px
        border: none
        background: #00A7A7D9
        padding: 10px 30px
        margin-top: 20px
        cursor: pointer
        color: white
        width: max-content

    @media screen and (min-width: $medium) and (max-width: $large)
        .txtbox
            font-size: 1rem

        .button
            font-size: 1rem

    @media screen and (min-width: $small) and (max-width: $medium)
        .txtbox
            font-size: 0.75rem

        .button
            font-size: 0.75rem

    @media screen and (max-width: $small)
        .txtbox
            font-size: 0.50rem
            padding: 10px
            margin: 10px 0
        .button
            font-size: 0.5rem
            margin-top: 10px
</style>
