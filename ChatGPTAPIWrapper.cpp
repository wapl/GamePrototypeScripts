// Fill out your copyright notice in the Description page of Project Settings.


#include "ChatGPTAPIWrapper.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Misc/ConfigCacheIni.h"

UChatGPTAPIWrapper::UChatGPTAPIWrapper()
{
}

UChatGPTAPIWrapper::~UChatGPTAPIWrapper()
{
}

void UChatGPTAPIWrapper::SetOpenAIAPIKey(const FString& ApiKey)
{
	OpenAIAPIKey=ApiKey;
}

FString UChatGPTAPIWrapper::GetOpenAIAPIKey()
{
	if(!OpenAIAPIKey.IsEmpty())
	{
		return OpenAIAPIKey;
	}
	FString ApiKey;
	if(GConfig->GetString(TEXT("OpenAi"),TEXT("APIKey"),ApiKey,GEngineIni))
	{
		return ApiKey;
	}
	return TEXT("");
}

void UChatGPTAPIWrapper::SendRequest(const FString& Prompt, const FonSuccessDelegate& OnSuccess, const FOnErrorDelegate& OnError)
{
	FString APIKey=GetOpenAIAPIKey();
	if(!APIKey.IsEmpty())
	{
		FHttpModule* Http=&FHttpModule::Get();
		TSharedRef<IHttpRequest,ESPMode::ThreadSafe> Request=Http->CreateRequest();
		Request->OnProcessRequestComplete().BindUObject(this,&UChatGPTAPIWrapper::OnResponseRecieved,OnSuccess,OnError);
		Request->SetURL("https://subjective-gm-beautifully-fw.trycloudflare.com/api/v1/generate");
		
		Request->SetVerb("POST");
		Request->SetHeader("Content-Type","application/json");
		//Request->SetHeader("Authorization",FString::Printf(TEXT("Bearer %s"),*APIKey));
		
		TSharedPtr<FJsonObject>JsonRequestObject=MakeShareable(new FJsonObject);
		JsonRequestObject->SetStringField("prompt",Prompt);
		//JsonRequestObject->SetNumberField("max_tokens",MaxTokens);
		JsonRequestObject->SetNumberField("Temperature",Temperature);
		JsonRequestObject->SetNumberField("top_p",TopP);

		FString JsonPayload;
		TSharedRef<TJsonWriter<>> JsonWriter=TJsonWriterFactory<>::Create(&JsonPayload);
		FJsonSerializer::Serialize(JsonRequestObject.ToSharedRef(),JsonWriter);
		Request->SetContentAsString(JsonPayload);
		Request->ProcessRequest();
		
	}
	else
	{
		OnError.Execute(-1,TEXT("Api Key not found or invalid"));
		
	}
	
}
void UChatGPTAPIWrapper::OnResponseRecieved(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful, FonSuccessDelegate OnSuccess, FOnErrorDelegate OnError)
{
	
	
	if (bWasSuccessful && Response.IsValid())
	{
		if(Response->GetResponseCode()==200)
		{
			TSharedPtr<FJsonObject>JsonObject;
			TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<> ::Create(Response->GetContentAsString());
			if(FJsonSerializer::Deserialize(Reader,JsonObject))
			{
				TArray<TSharedPtr<FJsonValue>> Choices=JsonObject->GetArrayField("results");
				if(Choices.Num()>0)
				{
					TSharedPtr<FJsonObject> ChoiceObject=Choices[0]->AsObject();
					FString GeneratedText=ChoiceObject->GetStringField("text");
					OnSuccess.Execute(GeneratedText);
				}
				else
				{
					OnError.Execute(Response->GetResponseCode(),TEXT("No Choices were returned by the API"));
				}
			}
			else
			{
				OnError.Execute(Response->GetResponseCode(),TEXT("Failed to parse the JSON response"));
			}
		}
		OnError.Execute(Response->GetResponseCode(),FString::Printf(TEXT("API returned an error ,Response code: %d "),Response->GetResponseCode()));
	}
	else
	{
		OnError.Execute(-1,TEXT("Failed to connect to the OpenAI API"));
	}
}


