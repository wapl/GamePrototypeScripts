// Fill out your copyright notice in the Description page of Project Settings.


#include "CluesActor.h"

#include "IPropertyTable.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "Runtime/UMG/Public/UMG.h"
#include "Runtime/UMG/Public/UMGStyle.h"
#include "Runtime/UMG/Public/Slate/SObjectWidget.h"
#include "Runtime/UMG/Public/IUMGModule.h"
#include "Runtime/UMG/Public/Blueprint/UserWidget.h"
#include "Slate.h"
#include "Math/UnrealMathUtility.h"

// Sets default values
ACluesActor::ACluesActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	
	clueMesh=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
	clueMesh->SetupAttachment(RootComponent);

	clueMesh->SetRelativeLocation(FVector(0.0f,0.0f,0.0f));

	clueCollider=CreateDefaultSubobject<UBoxComponent>(TEXT("Clue Collider") );
	clueCollider->SetupAttachment(clueMesh);
	clueCollider->SetRelativeLocation(FVector(0.0f,0.0f,0.0f));
	clueCollider->SetRelativeScale3D(FVector(2.0f,2.0f,2.0f));

	clueCollider->OnComponentBeginOverlap.AddDynamic(this,&ACluesActor::OnOverlapBegin);
	clueCollider->OnComponentEndOverlap.AddDynamic(this,&ACluesActor::OnOverlapEnd);
	//PC=UGameplayStatics::GetPlayerController(GetWorld(), 0);
	
	
	ConstructorHelpers::FClassFinder<UUserWidget>CluePromptBPClass(TEXT("/Game/blueprints/CluePrompt"));
	
	cluePromptUI=CluePromptBPClass.Class;

	
	//ConstructorHelpers::FObjectFinder<UStruct>clueDt(TEXT("/Game/blueprints/CluesStruct"));
	
	//clueTable=clueDt.Object;
	
	//InputComponent->BindKey(EKeys::E, IE_Pressed, this, &Contoller::AReleased);
}

// Called when the game starts or when spawned
void ACluesActor::BeginPlay()
{
	Super::BeginPlay();
	clueRef=CreateWidget<UUserWidget>(GetWorld(),cluePromptUI,"CluePrompt");
	
	
	
	PC=GetWorld()->GetFirstPlayerController();
	
	
	collided=false;
}

// Called every frame
void ACluesActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if(PC!=nullptr)
	{
		//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("Player controller found"));
		if(PC->WasInputKeyJustPressed(EKeys::E) && collided )
		{
			if(GEngine)
				GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("E Pressed "));
			FName TestUiName = FName(TEXT("ClueText"));
			Cast<UTextBlock>(clueRef->GetWidgetFromName(TestUiName))->SetText(FText::FromString(clueText));
			clueRef->AddToViewport();
		}
	
	}
	else
	{
		//GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("Not Found"));
	}
	
	
	
}
void ACluesActor::OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	

	if(OtherActor && (OtherActor !=PC) )
	{
		if(GEngine)
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("Enter!"));
		collided=true;
	}
	
}
void ACluesActor::OnOverlapEnd(UPrimitiveComponent* OverlappedComp, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if(OtherActor && (OtherActor !=PC) )
	{
		if(GEngine)
			GEngine->AddOnScreenDebugMessage(-1, 15.0f, FColor::Yellow, TEXT("Exit!"));	
		collided=false;
		clueRef->RemoveFromViewport();
	}
	
}






