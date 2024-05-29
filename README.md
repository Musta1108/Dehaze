# Report

**Dark Channel Prior (DCP) Dehazing Algorithm**

The Dark Channel Prior (DCP) dehazing algorithm relies on the atmospheric scattering model to remove haze from images. By observing and summarizing a large number of hazy and haze-free images, certain mapping relationships are identified. These relationships are then used to reverse the haze formation process, thereby recovering clear images.

![Dehazing Example](https://img-blog.csdnimg.cn/e1bde38155b046828fb13ee0309fbb79.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

### (1) Atmospheric Scattering Model

In computer vision and computer graphics, the atmospheric scattering model described by the equation is widely used. The parameters are defined as follows:

- \(x\): Spatial coordinate of the image
- \(I(x)\): Hazy image (image to be dehazed)
- \(J(x)\): Haze-free image (image to be recovered)
- \(A\): Global atmospheric light value
- \(t(x)\): Transmission rate

The equation represents the scene radiance, where the first term on the right side is the direct attenuation of the scene, and the second term is the atmospheric light.

![Atmospheric Scattering Model](https://img-blog.csdnimg.cn/acc445eff5a84c27a4026f1e9c505f44.png#pic_center)

### (2) Dark Channel Definition

In most non-sky local regions, some pixels always have very low values in at least one color channel. For an image \(J(x)\), the mathematical definition of its dark channel is expressed as:

![Dark Channel Definition](https://img-blog.csdnimg.cn/46432e67aecb4d029689a0ce72212ecf.png#pic_center)

Where \(Ω(x)\) represents the local patch centered at \(x\), and the superscript \(c\) denotes the RGB channels. The meaning of this formula is simple when expressed in code: first, find the minimum value among the RGB components for each pixel, store these values in a grayscale image of the same size as the original image, and then apply a minimum filter with a radius determined by the window size.

### (3) Dark Channel Prior Theory

The dark channel prior theory states that for haze-free images \(J(x)\) in non-sky regions, the dark channel is close to zero:

![Dark Channel Prior](https://img-blog.csdnimg.cn/4ee0c04294e84a30b265933bb41ff1af.png#pic_center)

In real life, the low values in the dark channel are mainly caused by three factors:

a) Shadows of objects such as cars, buildings, windows, or natural features like leaves, trees, and rocks.
b) Colorful objects or surfaces that have low values in some channels (e.g., green grass/trees/plants, red or yellow flowers/leaves, or blue water surfaces).
c) Dark-colored objects or surfaces, such as tree trunks and stones.

![Dark Channel Theory](https://img-blog.csdnimg.cn/b12dc4e35c6e4c26a16971b6051f8485.png?x-oss-process%3Dimage%2Fwatermark%2Ctype_ZHJvaWRzYW5zZmFsbGJhY2s%2Cshadow_50%2Ctext_Q1NETiBARWFzdG1vdW50%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16#pic_center)

Thus, shadows and colors are ubiquitous in natural scenes, and their images’ dark channels are generally dark, whereas hazy images are relatively brighter. Hence, the dark channel prior theory is quite universal.

### (4) Formula Transformation

According to the atmospheric scattering model, we can slightly transform the first equation into:

![Transformed Formula](https://img-blog.csdnimg.cn/40090d06199343da95460bd1f8c5d178.png#pic_center)

Assuming the transmission rate \(t(x)\) within each patch is constant, denoted as \(t’(x)\), and the value of \(A\) is known, applying minimum filtering to both sides of the equation yields:

![Min Filter](https://img-blog.csdnimg.cn/910ee44d94ab4fcbbfdb5a89c9da92d0.png#pic_center)

Where \(J(x)\) is the desired haze-free image. According to the dark channel prior theory:

![Dark Channel Zero](https://img-blog.csdnimg.cn/e2c744f21b334fc6bd0e7a949d1280e4.png#pic_center)

We can deduce:

![Deduced Formula](https://img-blog.csdnimg.cn/0d02d7f93b7e47ef8de9416726f235dc.png#pic_center)

### (5) Transmission Rate Calculation

By substituting the above equation, we obtain the estimated value of the transmission rate \(t’(x)\):

![Transmission Rate Estimation](https://img-blog.csdnimg.cn/383f3b7436ed4f0f91c7c07c99c0b652.png#pic_center)

In real-life scenarios, even on clear days, there are still particles in the air, making distant objects appear slightly hazy. The presence of haze provides a sense of depth; thus, it is necessary to retain some haze while dehazing. This can be done by introducing a factor \(w\) (usually 0.95) to modify the estimated transmission rate:

![Modified Transmission Rate](https://img-blog.csdnimg.cn/a8fb67d3051a4ab5a0aac526dbf4f4de.png#pic_center)

The above derivation assumes that the atmospheric light \(A\) is known. In practice, it can be estimated from the original hazy image using the dark channel image. The steps are as follows:

1. Compute the dark channel image and extract the brightest 0.1% pixels.
2. In the original hazy image \(I(x)\), find the highest intensity pixels corresponding to these locations to determine the atmospheric light \(A\).

Moreover, when the transmission rate \(t\) is low, \(J\) tends to be high, causing the dehazed image to appear overly bright. Therefore, it is necessary to set a lower bound \(t_0\) (usually 0.1) for the transmission rate. When \(t\) is less than \(t_0\), set \(t = t_0\). Substituting the obtained transmission rate and atmospheric light into the formula, we get the final image recovery formula:

![Final Recovery Formula](https://img-blog.csdnimg.cn/79825f7520f045619b57b3cd78c04e81.png#pic_center)

This is the principle of the Dark Channel Prior dehazing algorithm.
