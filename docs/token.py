from blacksheep.server.openapi.common import (
    ContentInfo,
    EndpointDocs,
    HeaderInfo,
    RequestBodyInfo,
    ResponseExample,
    ResponseInfo,
)
from domain.token import Chain, Token, CreateTokenInput, UpdateTokenInput, DeleteTokenInput, UpdateURLInput

create_token = EndpointDocs(
    summary="Add a new token into a group chat",
    request_body=RequestBodyInfo(
        examples={
            "token": CreateTokenInput(
                token_address="0xe9e7cea3dedca5984780bafc599bd69add087d56",
                chain=Chain.BSC,
                chat_id=-1001612967544
            ),
        },
    ),
    responses={
        200: ResponseInfo(
            "Successfully add a new token into a group chat",
            content=[
                ContentInfo(
                    Token,
                    examples=[
                        ResponseExample(
                            {
                                'message': "Pair Added"
                            }
                        )
                    ],
                )
            ],
        ),
        400: "Pair Already Added",
        422: "Please input valid Token Address!"
    },
)

update_tokens = EndpointDocs(
    summary="Update token notification",
    request_body=RequestBodyInfo(
        examples={
            "pausing_token_notification": UpdateTokenInput(
                group_id='6347be27293b2388b9db1f93',
                is_paused=True,
            ),
            "resuming_token_notification": UpdateTokenInput(
                group_id='6347be27293b2388b9db1f93',
                is_paused=False,
            ),
        },
    ),
    responses={
        200: ResponseInfo(
            "Successfully pausing / resuming token notification",
            content=[
                ContentInfo(
                    Token,
                    examples=[
                        ResponseExample(
                            {
                                'message': "Token buy notification successfully paused!"
                            }
                        )
                    ],
                )
            ],
        ),
    },
)

update_token = EndpointDocs(
    summary="Update token notification",
    request_body=RequestBodyInfo(
        examples={
            "pausing_token_notification": UpdateTokenInput(
                group_id='6347be27293b2388b9db1f93',
                is_paused=True,
            ),
            "resuming_token_notification": UpdateTokenInput(
                group_id='6347be27293b2388b9db1f93',
                is_paused=False,
            ),
        },
    ),
    responses={
        200: ResponseInfo(
            "Successfully pausing / resuming token notification",
            content=[
                ContentInfo(
                    Token,
                    examples=[
                        ResponseExample(
                            {
                                'message': "Token buy notification successfully paused!"
                            }
                        )
                    ],
                )
            ],
        ),
    },
)

delete_token = EndpointDocs(
    summary="Removing token from a group chat",
    request_body=RequestBodyInfo(
        examples={
            "removing_token": DeleteTokenInput(
                group_id='6347be27293b2388b9db1f93',
            ),
        },
    ),
    responses={
        200: ResponseInfo(
            "Successfully remove token from a group chat",
            content=[
                ContentInfo(
                    Token,
                    examples=[
                        ResponseExample(
                            {
                                'message': "Token successfully deleted!"
                            }
                        )
                    ],
                )
            ],
        ),
    },
)

delete_tokens = EndpointDocs(
    summary="Removing all tokens from a group chat",
    request_body=RequestBodyInfo(
        examples={
            "removing_token": DeleteTokenInput(
                group_id='6347be27293b2388b9db1f93',
            ),
        },
    ),
    responses={
        200: ResponseInfo(
            "Successfully remove all tokens from a group chat",
            content=[
                ContentInfo(
                    Token,
                    examples=[
                        ResponseExample(
                            {
                                'message': "Token successfully deleted!"
                            }
                        )
                    ],
                )
            ],
        ),
    },
)

change_ads = EndpointDocs(
    summary="Change Ads URL in group chat"
)

delete_ads = EndpointDocs(
    summary="Removing Ads URL in group chat"
)

update_min_buy = EndpointDocs(
    summary="Changing minimum buy to show token notification"
)

update_emoji = EndpointDocs(
    summary="Changing emoji to show on token notification"
)

update_telegram = EndpointDocs(
    summary="Change Telegram URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://t.me/soji_shim",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_telegram = EndpointDocs(
    summary="Removing Telegram URL in token notification"
)

update_presale = EndpointDocs(
    summary="Change Presale URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://www.pinksale.finance/launchpad/0x13f625ad1bb28c57beb4c0c5ace302f695cc83dd?chain=BSC",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_presale = EndpointDocs(
    summary="Removing Presale URL in token notification"
)

update_chart = EndpointDocs(
    summary="Change Chart URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://poocoin.app/",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_chart = EndpointDocs(
    summary="Removing Chart URL in token notification"
)

update_discord = EndpointDocs(
    summary="Change Discord URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://discord.gg/",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_discord = EndpointDocs(
    summary="Removing Discord URL in token notification"
)

update_twitter = EndpointDocs(
    summary="Change Twitter URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://twitter.com/",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_twitter = EndpointDocs(
    summary="Removing Twitter URL in token notification"
)

update_website = EndpointDocs(
    summary="Change Twitter URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://www.matakala.io/",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_website = EndpointDocs(
    summary="Removing Twitter URL in token notification"
)

update_image = EndpointDocs(
    summary="Change Image URL in token notification",
    request_body=RequestBodyInfo(
        examples={
            "changing url": UpdateURLInput(
                url="https://res.cloudinary.com/dx5hwvab6/image/upload/v1666265495/Banner_shil_ofls2u.png",
                group_id='6347be27293b2388b9db1f93',
                token_id='6350ef9f5b2c7cea3e6ea61a',
            ),
        },
    ),
)

delete_image = EndpointDocs(
    summary="Removing Image URL in token notification"
)

update_content = EndpointDocs(
    summary="Change Content in token notification"
)

delete_content = EndpointDocs(
    summary="Removing Content in token notification"
)
