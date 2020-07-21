from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock

from wagtail.core import blocks

from wagtail_blocks.blocks import HeaderBlock, ListBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, ListWithImagesBlock, ThumbnailGalleryBlock, ChartBlock, MapBlock, ImageSliderBlock


class ConflictosStreamBlock(StreamBlock):
    # paragraph_block = RichTextBlock(icon="fa-paragraph", template="blocks/paragraph_block.html")
    paragraph_block = RichTextBlock()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html"
    )
    header_block = HeaderBlock()
    list_block = ListBlock()
    image_text_overlay_block = ImageTextOverlayBlock()
    cropped_images_with_text_block = CroppedImagesWithTextBlock()
    list_with_images_block = ListWithImagesBlock()
    thumbnail_gallery_block = ThumbnailGalleryBlock()
    chart_block = ChartBlock()
    map_block = MapBlock()
    image_slider_block = ImageSliderBlock()
