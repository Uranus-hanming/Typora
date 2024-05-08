## npm 支持



### 1. 构建 npm



目前小程序已经支持使用 npm 安装第三方包，但是这些 npm 包在小程序中不能够直接使用，必须得使用小程序开发者工具进行构建后才可以使用。



**`为什么得使用小程序开发者工具需要构建呢❓`**



因为 `node_modules` 目录下的包，不会参与小程序项目的编译、上传和打包，因此。在小程序项目中要想使用 npm 包，必须走一遍 **构建 npm** 的过程。



在构建成功以后，默认会在小程序项目根目录，也就是 `node_modules` 同级目录下生成 `miniprogram_npm`目录，里面存放这构建打包后的 npm 包，也就是小程序运行过程中真正使用的包



<img src="http://8.131.91.46:6677/mina/base/构建完成.jpg" style="zoom:80%;" />



**`微信开发者工具如何构建❓`**



我们以使用 [Vant Weapp](https://vant-contrib.gitee.io/vant-weapp/#/home) 小程序 UI 组件库为例，来说明小程序如何安装和构建 npm，构建 npm 的步骤如下：



1. 初始化 `package.json`
2. 通过 `npm` 安装项目依赖
3. 通过微信开发者工具构建 `npm`



> 📌 **注意事项**：
>
> 1. 小程序运行在微信内部，因为运行环境的特殊性，这就导致 并不是所有的包都能够在小程序使用
>2. 我们在小程序中提到的包指专为小程序定制的 npm 包，简称小程序 npm 包，在使用包前需要先确定该包是否支持小程序
> 
>3. 开发者如果需要发布小程序包，需要参考官方规范：[https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html#发布-npm-包](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html#发布-npm-包)



**构建的详细步骤：**



1. 初始化 `package.json`，**这一步至关重要，要不然后续的步骤都很难进行下去**

   ```shell
   npm init -y
   ```

   <img src="http://8.131.91.46:6677/mina/base/46-初始化package.jpg" style="zoom:80%;" />

   

2. 通过 npm 安装 `@vant/weapp` 包

   ```shell
   npm i @vant/weapp -S --production
   ```

   ![](http://8.131.91.46:6677/mina/base/vant-weapp.jpg)

   

3. 构建 npm

   <img src="http://8.131.91.46:6677/mina/base/构建vant-weapp.jpg" style="zoom:60%;" />

   <img src="http://8.131.91.46:6677/mina/base/vant 构建完成.jpg" style="zoom:67.8%;" />



4. 修改 app.json

   到这一步 npm 的构建已经完成了，但是 `Vant` 组件库，会和基础组件的样式冲突，因此我们需要继续往下配置

   将 app.json 中的 `"style": "v2"` 去除，小程序的[新版基础组件](https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html#style)强行加上了许多样式，难以覆盖，不关闭将造成部分组件样式混乱。

   

5. 在页面中使用 `vant` 提供的小程序组件，这里以 `Button` 按钮组件为例

   - 在`app.json`或`index.json`中引入组件
   - 在 `app.json` 中注册的组件为全局注册，可以在任意组件中进行使用
   - 在 `index.json` 中注册组件为组件组件，只能在当前组件中进行使用
   - 按照组件提供的使用方式，在页面中使用即可

   ```json
   "usingComponents": {
     "van-button": "@vant/weapp/button/index"
   }
   ```

   ```html
   <van-button type="default">默认按钮</van-button>
   <van-button type="primary">主要按钮</van-button>
   <van-button type="info">信息按钮</van-button>
   <van-button type="warning">警告按钮</van-button>
   <van-button type="danger">危险按钮</van-button>
   ```

   

6. 页面预览效果

<img src="http://8.131.91.46:6677/mina/base/vant 组件库.jpg" style="zoom:60%; border: 1px solid #ccc" />









### 2. 自定义构建 npm



在实际的开发中，随着项目的功能越来越多、项目越来越复杂，文件目录也变的很繁琐，为了方便进行项目的开发，开发人员通常会对目录结构进行调整优化，例如：将小程序源码放到 miniprogram 目录下。



但是在调整目录以后，我们按照上一小节 `Vant Weapp` 的构建流程进行构建，发现没有构建成功，并且弹出构建失败的弹框

<img src="http://8.131.91.46:6677/mina/base/构建失败.jpg" style="zoom:76%;" />



[错误提示翻译意思是] ：没有找到可以构建的 npm 包

[解决方式]：

1. 请确认需要参与构建的 npm 都在 `miniprogramRoot` 目录内
2. 配置 `project.config.json` 的 `packNpmManually` 和 `packNpmRelationList` 进行构建



产生这个错误的原因是因为小程序的构建方式有两种：

1. 默认构建 `npm`
2. 自定义构建 `npm`



**`默认构建 npm`**



默认情况下，不使用任何模版，`miniprogramRoot` 是小程序项目根目录，在 `miniprogramRoot` 内正确配置了 `package.json` 并执行 `npm install` 之后，在项目的根目录下就有 `node_modules` 文件夹，然后对 `node_modules` 中的 `npm` 进行构建，其构建 npm 的结果是，为 `package.json` 对应的 `node_modules` 构建一份 `miniprogram_npm`，并放置在对应 `package.json `所在目录的子目录中



**`自定义构建 npm`**



与`默认的构建 npm 方式`不一样，自定义构建 npm 的方式为了更好的优化目录结构，更好的管理项目中的代码。

需要开发者在 `project.config.json` 中指定 `node_modules` 的位置 和 目标 `miniprogram_npm` 的位置



在`project.config.json`中详细的配置流程和步骤如下：



1. 新增 `miniprogramRoot` 字段，指定调整后了的小程序开发目录
2. 新增 `setting.packNpmManually`设置为 `true`，开启指定`node_modules` 的位置以及构建成功后文件的位置
3. 新增 `setting.packNpmRelationList` 项，指定 `packageJsonPath` 和 `miniprogramNpmDistDir` 的位置
   - `packageJsonPath` 表示 `node_modules` 源对应的 `package.json`
   - `miniprogramNpmDistDir` 表示 `node_modules` 的构建结果目标位置



```json
{
  // 指定调整后了的小程序开发目录
  "miniprogramRoot": "miniprogram/",
  "setting": {
    // 开启自定义 node_modules 和 miniprogram_npm 位置的构建 npm 方式
    "packNpmManually": true,
    // 指定 packageJsonPath 和 miniprogramNpmDistDir 的位置
    "packNpmRelationList": [
      {
        "packageJsonPath": "./package.json",
        "miniprogramNpmDistDir": "./miniprogram"
      }
    ]
  }
}
```





**落地代码：**



1. 将小程序核心源码放到 miniprogram 目录下

2. 在`project.config.json`中进行配置

   ```json
   {
     "compileType": "miniprogram",
    
   +   "miniprogramRoot": "miniprogram/",
   +   "setting": {
   +     "packNpmManually": true,
   +     "packNpmRelationList": [
   +       {
   +         "packageJsonPath": "./package.json",
   +         "miniprogramNpmDistDir": "./miniprogram"
   +       }
   +     ]
   +   }
       
     // coding... 其他配置项
   }
   ```

   







### 3. Vant 组件的使用方式



Vant Weapp 是有赞前端团队开源的小程序 UI 组件库，基于微信小程序的自定义组件开发，可用来快速搭建小程序项目。



在使用 Vant 提供的组件时，只需要两个步骤：

1.将组件在 app.json 中进行全部注册 或者 index.json 中进行局部注册

2.在引入组件后，可以在 wxml 中直接使用组件



在前面我们以 `image` 组件为例，讲解 `Vant` 组件库的基本使用方式



首先还是需要将先将组件进行引入，这里我们进行全局引入

```json
// app.json

"usingComponents": {
  "van-image": "@vant/weapp/image/index"
}
```



引入组件后，可以在 wxml 中直接使用组件

```html
<van-image width="100" height="100" src="https://img.yzcdn.cn/vant/cat.jpeg" />

<!-- 坑： -->
<!-- 在使用 van-image 图片组件时，如果需要渲染本地的图片，不能使用 ../ -->
<!-- 需要相对于小程序源码的目录来查找图片才可以 -->
<!-- <van-image width="100" height="100" src="../../assets/Jerry.png" /> -->
```



如果我们想给 `van-field` 添加一些属性，这时候我们需要查看 [API 手册](https://vant-contrib.gitee.io/vant-weapp/#/image#props)

```html
<van-image width="100" height="100" round src="/assets/Jerry.png"/>

```



如果我们想给 `van-field` 添加一些事件，这时候我们需要查看 [事件 手册](https://vant-contrib.gitee.io/vant-weapp/#/image#tu-pian-tian-chong-mo-shi)

```html
<van-image
  width="100"
  height="100"
  round
  src="/assets/Jerry.png"
  bind:click="imageHandler"
/>

```

```js
Page({

  imageHandler () {
    console.log('点击图片时触发点击事件，执行该事件处理函数~~~~')
  }

}
```



如果我们想给 `van-field` 添加一些插槽，这时候我们需要查看 [slot 手册](https://vant-contrib.gitee.io/vant-weapp/#/image#slots)

```html
<van-image
  width="100"
  height="100"
  round
+   use-loading-slot
+   use-error-slot
  src="/assets/Jerry.png"
  bind:click="imageHandler"
>
+   <!-- slot: loading -->
+   <van-loading slot="loading" type="spinner" size="20" vertical />
+ 
+   <!-- slot: error -->
+   <text slot="error">加载失败</text>
</van-image>

```



如果我们想给 `van-field` 添加一些外部样式类，这时候我们需要查看 [外部样式类 手册](https://vant-contrib.gitee.io/vant-weapp/#/image#wai-bu-yang-shi-lei)

```html
<van-image
  width="100"
  height="100"
  round
  use-loading-slot
  use-error-slot
+   custom-class="custom-class"
  src="/assets/Jerry.png"
  bind:click="imageHandler"
>
  <!-- slot: loading -->
  <van-loading slot="loading" type="spinner" size="20" vertical />

  <!-- slot: error -->
  <text slot="error">加载失败</text>
</van-image>

```



```scss
/* pages/index/index.wxss */

.custom-class {
  border: 10rpx solid lightseagreen !important;
}
```









### 4. Vant 组件的样式覆盖



`Vant Weapp` 基于微信小程序的机制，为开发者提供了以下 3 种修改组件样式的方法



1. 解除样式隔离：在页面中使用 Vant Weapp 组件时，可直接在页面的样式文件中覆盖样式
2. 使用外部样式类：需要注意普通样式类和外部样式类的优先级是未定义的，需要添加 !important 保证外部样式类的优先级
3. 使用 CSS 变量：在页面或全局对多个组件的样式做批量修改以进行主题样式的定制



**`第 1 种：解除样式隔离`**



`Vant Weapp` 的所有组件都开启了`addGlobalClass: true`以接受外部样式的影响，因此我们可以通过审核元素的方式获取当前元素的类名，然后复制到组件的 `.wxss` 中进行修改

<img src="http://8.131.91.46:6677/mina/base/接触样式隔离.jpg" style="zoom:80%;" />





**`第 2 种：使用外部样式类`**



`Vant Weapp` 开放了大量的外部样式类供开发者使用，具体的样式类名称可查阅对应组件的 “外部样式类” 部分。

需要注意的是普通样式类和外部样式类的优先级是未定义的，因此使用时请添加`!important`以保证外部样式类的优先级。

<img src="http://8.131.91.46:6677/mina/base/自定义样式类.jpg" style="zoom:80%; border: 1px solid #ccc" />



**`第 3 种：使用 CSS 变量`**



`Vant Weapp` 可以通过 `CSS` 变量的方式多个组件的样式做批量修改。`CSS` 的变量基础用法如下：



1. 声明一个自定义属性，属性名需要以两个减号（`--`）开始，属性值则可以是任何有效的 CSS 值

```css
/* app.wxss */

/* 声明全局的变量，可在项目中任意组件中使用 */
page {
  --main-bg-color: lightcoral;
}
```



2. 使用一个局部变量时用 [`var()`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/var) 函数包裹以表示一个合法的属性值

```css
/* 声明局部的变量 */
/* 只有被当前类名容器包裹住的元素，使用该变量才生效 */
.container {
  --main-bg-color: lightseagreen;
}

.custom-class {
  /* 使用一个局部变量时用 var() 函数一个合法的属性值 */
  background-color: var(--main-bg-color) !important;
  color: #fff !important;
}
```



3. 页面中使用该变量

```html
<view class="container">
  <van-button
    type="default"
    custom-class="custom-class"
  >
    默认按钮
  </van-button>
</view>

<van-button
  type="default"
  custom-class="custom-class"
>
  默认按钮
</van-button>
```



![](http://8.131.91.46:6677/mina/base/CSS 变量修改演示.jpg)



----



也可以在按钮身上添加类名：

```html
<!-- 使用 CSS 变量：如果需要再多个页面或者一个组件中 需要批量修改组件、定制主题 -->
<van-button type="primary" class="my-button">主要按钮</van-button>
```



```scss
.my-button {
  --color: rgb(221, 152, 24);
}

.van-button--primary {
  font-size: 28rpx !important;
  background-color: var(--color) !important;
  border: 1px solid var(--color) !important;
}

```





