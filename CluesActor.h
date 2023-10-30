// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include <string>


#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/BoxComponent.h"
#include "GameFramework/Actor.h"
#include "Runtime/UMG/Public/UMG.h"
#include "Runtime/UMG/Public/UMGStyle.h"
#include "Runtime/UMG/Public/Slate/SObjectWidget.h"
#include "Runtime/UMG/Public/IUMGModule.h"
#include "Runtime/UMG/Public/Blueprint/UserWidget.h"
#include "Slate.h"
#include "Engine/DataTable.h"
#include "CluesActor.generated.h"


UCLASS()
class MYGAME_API ACluesActor : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ACluesActor();
	UPROPERTY(VisibleAnywhere)
	UStaticMeshComponent* clueMesh;
	UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="CluesText")
	FString clueText;

	UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Collider")
	UBoxComponent* clueCollider;
	

	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult & SweepResult);
	
	
	UFUNCTION()
	void OnOverlapEnd(class UPrimitiveComponent* OverlappedComp, class AActor* OtherActor, class UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
	
	UPROPERTY()
	APlayerController* PC;
	
	UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="UI")
	TSubclassOf<UUserWidget> cluePromptUI;

	
	
	UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="dataRow")
	FDataTableRowHandle dataHandle;
	
	UPROPERTY()
	UUserWidget* clueRef;

	UPROPERTY()
	bool collided;


	
protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

};
